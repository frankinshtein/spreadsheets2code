#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

from xml.dom import minidom
from jinja2 import Environment, FileSystemLoader
import sys



def first_rest_split(st):
    items = st.split('_')
    first = items[0]
    rest = items[1:]
    return first, rest

class Language:
    def __init__(self, args):
        self.name = args.language
        self.classes = {}
        self.extension = ""
        self.prefix = args.prefix
        self.args = args


    def add_class(self, name, cls):
        self.classes[name] = cls

    def get_nice_class_name(self, column):
        first, rest = first_rest_split(column)
        ret = first.capitalize() + ''.join(word.capitalize() for word in rest)
        return self.prefix + ret

    def get_field_name(self, column):
        first, rest = first_rest_split(column)
        ret = first + ''.join(word.capitalize() for word in rest)
        return ret

    def get_class(self, name):
        if name in self.classes:
            return self.classes[name]

        return Class(name, self.get_nice_class_name(name), True)

    def create_field(self, name, tpstr):
        nice_name = self.get_field_name(name)

        tp = None

        if not tpstr:
            tp = self.get_class("string")

        if tpstr == "id":
            tp = self.get_class("string")

        if tpstr == 'string' or tpstr == 'str':
            tp = self.get_class("string")

        array = False
        if tpstr[0] == "[":
            array = True
            tpstr = tpstr[1:-1]

        if not tp:
            tp = self.get_class(tpstr)

        return Field(name, nice_name, tp, array)





def save_if_changed(name, content):

    print("saving {}".format(name))
    try:
        with open(name, "r") as rd:
            data = rd.read()
            if data == content:
                return
    except IOError:
        pass

    with open(name, "w") as rd:
        rd.write(content)



class Field:
    def __init__(self, name, nice_name, type, array):
        self.type = type
        self.name = name
        self.nice_name = nice_name
        self.array = array

class Class:
    def __init__(self, name, nice_name = None, custom = False):
        self.fields = []
        self.name = name
        self.has_id = False
        self.custom = custom
        if nice_name:
            self.nice_name = nice_name
        else:
            self.nice_name = name

def gen(args, xml_res_file, dest_folder):

    sys.path.append(os.path.join(os.path.dirname(__file__), "templates"))

    module = __import__(args.language)
    lang = module.create(args)

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

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

    for class_node in root.childNodes:
        if class_node.nodeType == class_node.TEXT_NODE:
            continue

        class_name = class_node.nodeName
        cls = Class(class_name, lang.get_nice_class_name(class_name))

        classes.append(cls)

        attrs = class_node.attributes.values()


        for attr in attrs:
            name = attr.name

            #skip preset field
            if "-" in name:
                continue

            field = lang.create_field(name, attr.value)
            cls.fields.append(field)

            if name == "id":
                cls.has_id = True


        buffer = io.StringIO()

        template_args = {"cls": cls, "lang":lang, "loader":loader}

        buffer.write(env.get_template("class").render(**template_args))
        save_if_changed(dest_folder + cls.nice_name + lang.extension, buffer.getvalue())

    classes_with_id = filter(lambda v: v.has_id, classes)
    classes_without_id = filter(lambda v: not v.has_id, classes)

    template_args = {"classes": classes, "classes_with_id": classes_with_id,
                     "classes_without_id": classes_without_id,
                     "lang": lang, "loader":loader}

    buffer = io.StringIO()
    buffer.write(env.get_template("loader").render(**template_args))
    save_if_changed(dest_folder + loader + lang.extension, buffer.getvalue())



if __name__ == "__main__":


    import argparse
    parser = argparse.ArgumentParser(
        description="generates code from exported xml")
    parser.add_argument("xml", help="xml file to process")
    parser.add_argument("-l", "--language", help="language", default="java")
    parser.add_argument("-p", "--package", help="com.package.name", default="com.package.name")
    parser.add_argument("--prefix", help="generated classes prefix", default="G")
    parser.add_argument("--loader", help="loader class name", default="Loader")
    parser.add_argument(
        "-d", "--dest", help="destination folder for generated classes", default=".")


    args = parser.parse_args()
    gen(args, args.xml, args.dest + "/")