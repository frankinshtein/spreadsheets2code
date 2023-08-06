import xml2code

class CSClass(xml2code.Class):
    def __init__(self, *args, **kwargs):
        xml2code.Class.__init__(self, *args, **kwargs)
        self.object_name = self.nice_name

    def set_object_name(self, name):
        self.object_name = name
        return self



def create(args):
    config = xml2code.Language(args)
    config.Class = CSClass
    config.add_class("string", CSClass("string"))
    config.add_class("int", CSClass("int"))
    config.add_class("float", CSClass("float"))
    config.add_class("double", CSClass("double"))
    bool_ = CSClass("bool")
    config.add_class("bool", bool_)
    config.add_class("boolean", bool_)

    config.extension = ".cs"

    return config

