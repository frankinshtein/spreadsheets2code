import xml2code

class CSClass(xml2code.Class):
    def __init__(self, *args, **kwargs):
        xml2code.Class.__init__(self, *args, **kwargs)
        self.object_name = self.nice_name


class CSLang(xml2code.Language):
    def __init__(self, *args, **kwargs):
        xml2code.Language.__init__(self, *args, **kwargs)

    def get_nice_class_name(self, column):
        return self.prefix + self.get_field_name(column)

    def get_field_name(self, column):
        items = column.split("_")
        ret = ''.join(word.capitalize() for word in items)
        return ret


def create(args):
    config = CSLang(args)
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
