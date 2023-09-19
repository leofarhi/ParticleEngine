import javalang
from Base import *

#Ce script sert à Traduire les Types Java en Types Python

def TranslateType(type):
    if type.name == "boolean":
        return "bool"
    elif type.name in ["byte","short","int","long"]:
        return "int"
    elif type.name in ["float","double"]:
        return "float"
    elif type.name == "char":
        return "str"
    elif type.name == "void":
        return "None"
    elif type.name == "String":
        return "str"
    elif type.name == "ArrayList":
        return "list"
    else:
        return None


def TranslateValue(value):
    if isinstance(value, javalang.tree.Literal):
        if value.value == "true":
            return "True"
        elif value.value == "false":
            return "False"
        elif value.value == "null":
            return "None"
        else:
            return value.value
    elif isinstance(value, javalang.tree.StringLiteral):
        return "\"" + value.value + "\""

def DeflautValue(type):
    if type == "bool":
        return "False"
    elif type == "int":
        return "0"
    elif type == "float":
        return "0.0"
    elif type == "str":
        return "\"\""
    elif type == "list":
        return "[]"
    elif type == "None":
        return "None"
    else:
        RaiseException(None, "Unknown type: " + type)