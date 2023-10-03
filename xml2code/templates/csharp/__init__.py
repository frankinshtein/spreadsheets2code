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
    config.add_class("string", xml2code.Class(config, "string"))
    config.add_class("int", xml2code.Class(config, "int"))
    config.add_class("float", xml2code.Class(config, "float"))
    config.add_class("double", xml2code.Class(config, "double"))

    bool_ = xml2code.Class(config, "bool")
    config.add_class("bool", bool_)
    config.add_class("boolean", bool_)

    config.extension = ".cs"

    return config
