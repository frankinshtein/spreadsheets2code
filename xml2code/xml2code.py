#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

from xml.dom import minidom
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import sys




class Class:
    def __init__(self, name, nice_name=None, custom=False):
        self.fields = []
        self.fields_without_id = []
        self.name = name
        self.has_id = False
        self.custom = custom
        self.use_additional_field = False
        if nice_name:
            self.nice_name = nice_name
        else:
            self.nice_name = name

    def has_field(self, name):
        names = list(map(lambda field: field.name, self.fields))
        return name in names


class Field:
    def __init__(self, name, nice_name, type:Class, array, named_list):
        self.type = type
        self.name = name
        self.nice_name = nice_name
        self.array = array
        self.named_list = named_list
        self.ext = False

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
        self.Class = Class

    def add_class(self, name, cls):
        self.classes[name] = cls
        return cls

    def get_nice_class_name(self, column):
        first, rest = first_rest_split(column)
        ret = first.capitalize() + ''.join(word.capitalize() for word in rest)
        return self.prefix + ret

    def get_field_name(self, column):
        first, rest = first_rest_split(column)
        first = first.casefold()
        ret = first + ''.join(word.capitalize() for word in rest)
        return ret

    def get_class(self, name):
        if name in self.classes:
            return self.classes[name]

        cls = self.Class(name, self.get_nice_class_name(name), True)

        if name in self.args.use_additional_field:
            cls.use_additional_field = True

        return cls

    def create_field(self, name, tpstr: str, make_nice_name):

        tp = None
        array = False

        if not tpstr:
            tp = self.get_class("string")
        else:
            if tpstr[0] == "[" and tpstr[-1] == "]":
                array = True
                tpstr = tpstr[1:-1]
            if tpstr.endswith("[]"):
                array = True
                tpstr = tpstr[0:-2]

            if tpstr in ids:
                tp = self.get_class("string")

            if tpstr == 'string' or tpstr == 'str':
                tp = self.get_class("string")

        named_list = False
        if "." in name:
            named_list = True
            left, right = name.split(".")
            name = left

        if not tp:
            tp = self.get_class(tpstr)

        nice_name = name
        if make_nice_name:
            nice_name = self.get_field_name(name)
        else:
            nice_name = name.lower()

        return Field(name, nice_name, tp, array, named_list)

    def make_fields(self, args, cls:Class, attrs):

        nice_fields = True

        if cls.name in self.args.not_nice_field:
            nice_fields = False


        if cls.name == "campaign_quest":
            pass

        for attr in attrs:
            name = attr.name

            # skip preset field
            if "-" in name:
                continue

            field = self.create_field(name, attr.value, nice_fields)
            if cls.has_field(field.name):
                print("skipped dublicate field '{}' in '{}'".format(name, cls.name))
                continue

            cls.fields.append(field)

            if name in ids:
                cls.has_id = True
            else:
                cls.fields_without_id.append(field)

            #if field.type.use_additional_field:
            #    field = self.create_field(name+"XXX", field.type.name, nice_fields)
            #    cls.fields.append(field)

        for ext in self.args.ext:
            # ext = ""
            # building.field:EngNotation
            (class_field_, type_) = ext.split(":")
            (class_, field_) = class_field_.split(".")
            if class_ == cls.name:
                field = Field(field_, field_, self.Class(type_), False, False)
                field.ext = True
                cls.fields.append(field)


def gen(args, xml_res_file, dest_folder):
    sys.path.append(os.path.join(os.path.dirname(__file__), "templates"))

    module = __import__(args.language)
    lang = module.create(args)

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

    for class_node in root.childNodes:
        if class_node.nodeType == class_node.TEXT_NODE:
            continue

        class_name = class_node.nodeName
        print(f"parsing {class_name}")
        cls = lang.Class(class_name, lang.get_nice_class_name(class_name))


        classes.append(cls)

        attrs = class_node.attributes.values()

        lang.make_fields(args, cls, attrs)

        template_args = {"cls": cls, "lang": lang, "loader": loader}

        buffer = io.StringIO()
        buffer.write(env.get_template("class").render(**template_args))
        save_if_changed(cls.nice_name + lang.extension, buffer.getvalue())

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
    parser.add_argument('--use_additional_field', action='append', help='extended class fields', default=[])
    parser.add_argument('--not_nice_field', action='append', help='not nice fields classes array', default=[])

    args = parser.parse_args(params)
    gen(args, args.xml, args.dest + "/")


if __name__ == "__main__":
    run(None)
