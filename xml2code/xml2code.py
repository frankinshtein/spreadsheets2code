#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

from xml.dom import minidom
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import sys


class Class:
    def __init__(self, lang: 'Language', name: str, custom=True):
        self.fields = []
        self.fields_without_id = []
        self.name = name
        self.has_id = False
        self.custom = custom
        self.use_additional_field = False
        self.xml_node = None
        self.lang = lang
        self.table_name = name

    def has_field(self, name):
        names = list(map(lambda field: field.name, self.fields))
        return name in names


class Field:
    def __init__(self, name: str,
                 clazz: Class,
                 is_array: bool,
                 table_type_name: str,
                 named_list):
        self.clazz = clazz
        self.name = name
        self.is_array = is_array
        self.named_list = named_list
        self.ext = False
        if clazz.custom:
            self.parse_method_name = f"ConfigFieldsParser.Parse_{table_type_name}"
        else:
            self.parse_method_name = f"loader.Parse_{table_type_name}"

        self.nice_name = clazz.lang.get_nice_field_name(name)


def first_rest_split(st):
    if st.startswith('_'):
        return "", [st]
    items = st.split('_')
    first = items[0]
    rest = items[1:]
    return first, rest


ids = ["id", "type"]


class Language:
    def __init__(self, args):
        self.name = args.language
        self.classes = {}
        self.extension = ""
        self.prefix = args.prefix
        self.args = args

    def add_class(self, name: str, cls: Class) -> Class:
        self.classes[name] = cls
        return cls

    def get_nice_class_name(self, column) -> str:
        first, rest = first_rest_split(column)
        ret = first.capitalize() + ''.join(word.capitalize() for word in rest)
        return self.prefix + ret

    def get_nice_field_name(self, column) -> str:
        return self.get_nice_class_name(column)

    def get_class(self, table_type: str) -> Class:
        return self.classes[table_type]

    def create_field(self, name: str, table_type_str: str) -> Field:

        clazz: Class | None = None
        is_array = False

        if not table_type_str:
            clazz = self.get_class("string")
            table_type_str = "string"
        else:
            if table_type_str[0] == "[" and table_type_str[-1] == "]":
                is_array = True
                table_type_str = table_type_str[1:-1]
            if table_type_str.endswith("[]"):
                is_array = True
                table_type_str = table_type_str[0:-2]

            if table_type_str in ids:
                clazz = self.get_class("string")

            if table_type_str == 'string' or table_type_str == 'str':
                clazz = self.get_class("string")

        named_list = False
        if "." in name:
            named_list = True
            left, right = name.split(".")
            name = left

        if not clazz:
            clazz = self.get_class(table_type_str)

        return Field(name, clazz, is_array, table_type_str, named_list)

    def make_fields(self, cls: Class, attrs) -> None:

        for attr in attrs:
            name = attr.name

            # skip preset field
            if "-" in name:
                continue

            field = self.create_field(name, attr.value)
            if cls.has_field(field.name):
                print("skipped duplicate field '{}' in '{}'".format(name, cls.name))
                continue

            cls.fields.append(field)

            if name in ids:
                cls.has_id = True
            else:
                cls.fields_without_id.append(field)


"""
        for ext in self.args.ext:
            # ext = ""
            # building.field:EngNotation
            (class_field_, type_) = ext.split(":")
            (class_, field_) = class_field_.split(".")
            if class_ == cls.name:
                field = Field(field_, Class(self, type_), False, False)
                field.ext = True
                cls.fields.append(field)
"""


def gen(args, xml_res_file, dest_folder):
    sys.path.append(os.path.join(os.path.dirname(__file__), "templates"))

    module = __import__(args.language)
    lang: Language = module.create(args)

    dest_folder = os.path.join(dest_folder, args.generated)

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    listdir = os.listdir(dest_folder)

    xml_res_file = os.path.normpath(xml_res_file)
    xml_res_file = xml_res_file.replace("\\", "/")

    doc = minidom.parse(xml_res_file)
    root = doc.documentElement

    folder = os.path.split(__file__)[0] + "/templates/" + lang.name
    env = Environment(trim_blocks=True, lstrip_blocks=True,
                      loader=FileSystemLoader(folder))

    import io

    classes = []

    loader = args.prefix + args.loader

    def save_if_changed(save_class_name, content):
        if save_class_name in listdir:
            listdir.remove(save_class_name)
        save_class_name = os.path.join(dest_folder, save_class_name)
        print("saving {}".format(save_class_name))
        try:
            with open(save_class_name, "r") as rd:
                data = rd.read()
                if data == content:
                    return
        except IOError:
            pass

        with open(save_class_name, "w") as rd:
            rd.write(content)

    mapping: str
    for mapping in args.mapping:
        # minutes:TimeSpan
        (field_value, type_value) = mapping.split(':')
        cls = Class(lang, type_value, True)
        lang.classes[field_value] = cls

    for xml_node in root.childNodes:
        if xml_node.nodeType == xml_node.TEXT_NODE:
            continue

        class_name = xml_node.nodeName

        print(f"parsing {class_name}")
        cls = Class(lang, lang.get_nice_class_name(class_name), False)
        cls.xml_node = xml_node
        cls.table_name = class_name
        lang.classes[class_name] = cls

        if class_name in args.use_additional_field:
            cls.use_additional_field = True

        classes.append(cls)

    for cls in classes:
        fields = cls.xml_node.attributes.values()
        lang.make_fields(cls, fields)

        template_args = {"cls": cls, "lang": lang, "loader": loader}

        buffer = io.StringIO()
        buffer.write(env.get_template("class").render(**template_args))
        save_if_changed(cls.name + lang.extension, buffer.getvalue())

    classes_with_id = list(filter(lambda v: v.has_id, classes))
    classes_without_id = list(filter(lambda v: not v.has_id, classes))

    template_args = {"classes": classes, "classes_with_id": classes_with_id,
                     "classes_without_id": classes_without_id,
                     "lang": lang, "loader": loader}

    buffer = io.StringIO()
    buffer.write(env.get_template("loader").render(**template_args))
    save_if_changed(loader + lang.extension, buffer.getvalue())

    for item in listdir:
        name = os.path.join(dest_folder, item)
        if os.path.isfile(name):
            os.remove(name)


def run(params):
    import argparse

    parser = argparse.ArgumentParser(description="generates code from exported xml")
    parser.add_argument("xml", help="xml file to process")
    parser.add_argument("-l", "--language", help="language", default="java")
    parser.add_argument("-p", "--package", help="package/namespace", default="")
    parser.add_argument("--static_class", help="static class", default="")
    parser.add_argument("--prefix", help="generated classes prefix", default="")
    parser.add_argument("--loader", help="loader class name", default="Database")
    parser.add_argument("-d", "--dest", help="destination folder for generated classes", default=".")
    parser.add_argument("-g", "--generated", help="generated folder name, can't be empty or '.'", default="Generated")

    parser.add_argument('-e', '--ext', action='append', help='extended class fields', default=[])
    parser.add_argument('--mapping', action='append', help='fields remapping, example minutes:TimeSpan', default=[])
    parser.add_argument('--use_additional_field', action='append', help='extended class fields', default=[])
    parser.add_argument('--not_nice_field', action='append', help='not nice fields classes array', default=[])

    args = parser.parse_args(params)
    gen(args, args.xml, args.dest + "/")


if __name__ == "__main__":
    run(None)
