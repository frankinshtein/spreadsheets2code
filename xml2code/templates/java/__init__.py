import xml2code


def create(args):
    config = xml2code.Language(args)
    config.add_class("string", xml2code.Class("String"))
    config.add_class("int", xml2code.Class("int"))
    config.add_class("float", xml2code.Class("float"))
    config.add_class("double", xml2code.Class("double"))
    config.extension = ".java"

    return config

