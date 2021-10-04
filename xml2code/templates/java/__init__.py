import xml2code

class JavaClass(xml2code.Class):
    def __init__(self, *args, **kwargs):
        xml2code.Class.__init__(self, *args, **kwargs)
        self.object_name = self.nice_name

    def set_object_name(self, name):
        self.object_name = name
        return self



def create(args):
    config = xml2code.Language(args)
    config.Class = JavaClass
    config.add_class("string", JavaClass("String"))
    config.add_class("int", JavaClass("int").set_object_name("Integer"))
    config.add_class("float", JavaClass("float").set_object_name("Float"))
    config.add_class("double", JavaClass("double").set_object_name("Double"))

    bool_ = JavaClass("bool")
    config.add_class("bool", bool_)
    config.add_class("boolean", bool_)

    config.extension = ".java"

    return config

