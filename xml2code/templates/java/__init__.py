import xml2code



config = xml2code.Language("java")
config.add_class("string", xml2code.Class("String"))
config.add_class("int", xml2code.Class("int"))
config.add_class("float", xml2code.Class("float"))
config.add_class("double", xml2code.Class("double"))
