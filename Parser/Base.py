import ast
from Parser.Contents.ContentC import ContentC

DEBUG = True

class BaseParser:
    def __init__(self,nodeAST) -> None:
        pass

    def Compile(self) -> None:
        return
    
    def GetContent(self) -> ContentC:
        return ContentC()
    
    def PrintVariables(self) -> None:
        return
    
def GetType(name,node):
    name = str(name)
    if name in ["int","float","bool"]:
        return name
    if name == "str":
        return "unsigned char*"
    if name == "None":
        return "void"
    #check if is a class in the register
    ParserClass = BaseParser.Redirection[ast.ClassDef]
    CLASS = ParserClass.GetClassByName(name)
    if CLASS != None:
        return CLASS.name+"*"
    if "<" in name and ">" in name:
        firstName = name.split("<",1)[0]
        if firstName == "list":
            return "List*"
        if firstName == "dict":
            return "Dict*"
    RaiseException(node, "Unknown type "+name)

def GetValue(value):
    if isinstance(value, ast.Num):
        return str(value.n)
    if isinstance(value, ast.Str):
        return "\""+value.s+"\""
    if isinstance(value, ast.NameConstant):#True, False, None
        if value.value == None:
            return "NULL"
        if value.value == True:
            return "1"
        if value.value == False:
            return "0"
    if isinstance(value, ast.List):
        lst = []
        for el in value.elts:
            lst.append(GetValue(el))
        return "{"+",".join(lst)+"}"
    if isinstance(value, ast.Dict):
        lst = []
        for key in value.keys:
            lst.append(GetValue(key)+":"+GetValue(value.values[value.keys.index(key)]))
        return "{"+",".join(lst)+"}"
    RaiseException(value, "Unknown value "+str(value))
    
def RaiseException(node, msg):
    raise Exception(msg + " |#| in line " + str(node.lineno) + " and col " + str(node.col_offset))

Header_allowed = {
    "visibilities" : ["public", "private", "protected"],
    "UI_visibilities" : ["HideInInspector","SerializeField"],
    "static" : ["static"],
    "override" : ["override"],
    "virtual" : ["virtual"],
}

def GetAllowedHeader() -> list:
    lst = []
    for key in Header_allowed:
        lst += Header_allowed[key]
    return lst