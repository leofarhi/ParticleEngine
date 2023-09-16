import ast
import Parser.Base as Base
from Parser.Contents.ContentC import ContentC
from Parser.Base import GetAllowedHeader, Header_allowed
from Parser.Contents.ContentC import ContentC
from Parser.VariableDeclared import VariableDeclared


class ParserClass(Base.BaseParser):
    Register = []
    def GetParentClass(self):
        return ParserClass.GetClassByName(self.inheritance)
    def GetClassByName(name):
        for parserClass in ParserClass.Register:
            if parserClass.name == name:
                return parserClass
        return None
    def GetMethodByName(self, name):
        for method in self.methods:
            if method.name == name:
                return method
        return None
    def __init__(self, nodeAST):
        super().__init__(nodeAST)
        self.name = ""
        self.nodeAST = nodeAST
        self.attributes = [] #list of VariableDeclared
        #les attributs sont les variables de classe

        self.methods = [] #list of ParserFunction
        #les methodes sont les fonctions de classe

        self.inheritance = None #name
        #l'heritage est la classe mere

        self.constructor = None #ParserFunction
        #le constructeur est la fonction __init__

        self.destructor = None #ParserFunction
        #le destructeur est la fonction __del__

        ParserClass.Register.append(self)

    
    def Compile(self) -> None:
        if not isinstance(self.nodeAST, ast.ClassDef):
            Base.RaiseException(self.nodeAST, "The nodeAST must be a ClassDef")
        self.name = self.nodeAST.name
        if self.name.startswith("__"):
            Base.RaiseException(self.nodeAST, "The class name must not start with __")
        #check in register if already exist
        for parserClass in ParserClass.Register:
            if parserClass.name == self.name and parserClass != self:
                Base.RaiseException(self.nodeAST, "The class name already exist")
        #check inheritance (only one allowed)
        if len(self.nodeAST.bases) > 1:
            Base.RaiseException(self.nodeAST, "Only one inheritance is allowed")
        self.inheritance = self.nodeAST.bases[0].id if len(self.nodeAST.bases) == 1 else None
        #check attributes
        Header_settings = {"visibility": "private", "UI_visibility": None, "static": False, "override": False, "virtual": False}
        for node in self.nodeAST.body:
            if isinstance(node, ast.Expr):
                if isinstance(node.value, ast.List):
                    if len(node.value.elts) == 0:
                        Base.RaiseException(node, "The header must not be empty")
                    for elt in node.value.elts:
                        if isinstance(elt, ast.Constant):
                            if elt.value in GetAllowedHeader():
                                if elt.value in Header_allowed["visibilities"]:
                                    Header_settings["visibility"] = elt.value
                                elif elt.value in Header_allowed["UI_visibilities"]:
                                    if elt.value == "HideInInspector":
                                        Header_settings["UI_visibility"] = False
                                    elif elt.value == "SerializeField":
                                        Header_settings["UI_visibility"] = True
                                elif elt.value in Header_allowed["static"]:
                                    Header_settings["static"] = True
                            else:
                                Base.RaiseException(node, "Header not allowed")
                        else:
                            Base.RaiseException(node, "The header must be a string")
                else:
                    Base.RaiseException(node, "The header must be a list")
            #check if it is an attribute
            elif isinstance(node, ast.AnnAssign):
                if not isinstance(node.target, ast.Name):
                    Base.RaiseException(node, "The attribute must be a Name")
                if node.target.id.startswith("__"):
                    Base.RaiseException(node, "The attribute name must not start with __")
                #check if as a value
                if node.value == None:
                    Base.RaiseException(node, "The attribute must have a default value")
                if isinstance(node.annotation, ast.Call):#exemple :   a:list(int) = [1,2,3]
                    if not isinstance(node.annotation.func, ast.Name):
                        Base.RaiseException(node, "The attribute must be typed")
                    TYPE = str(node.annotation.func.id)+"<"
                    if len(node.annotation.args) == 0:
                        Base.RaiseException(node, "The attribute must be typed")
                    for arg in node.annotation.args:
                        if not isinstance(arg, ast.Name):
                            Base.RaiseException(node, "The attribute must be typed")
                        TYPE += str(arg.id)+","
                    TYPE = TYPE[:-1]+">"
                    variable = VariableDeclared(node, node.target.id, TYPE, node.value)                    
                elif isinstance(node.annotation, ast.Name):
                    variable = VariableDeclared(node, node.target.id, node.annotation.id, node.value)
                else:
                    Base.RaiseException(node, "The attribute must be typed")
                variable.visibility = Header_settings["visibility"]
                variable.UI_visibility = Header_settings["visibility"] == "public" if Header_settings["UI_visibility"] == None else Header_settings["UI_visibility"]
                variable.static = Header_settings["static"]
                self.attributes.append(variable)

                Header_settings["UI_visibility"] = None
                Header_settings["static"] = False
            #check if it is an attribute and raise an exception
            elif isinstance(node, ast.Assign):
                Base.RaiseException(node, "The attribute must be typed")
            #check if it is a method
            elif isinstance(node, ast.FunctionDef):
                #check if is constructor
                if node.name == "__init__":
                    #check if are not two constructors
                    if self.constructor != None:
                        Base.RaiseException(node, "Only one constructor is allowed")
                    parser = ParserClass.Redirection[ast.FunctionDef](node, self)
                    self.constructor = parser
                elif node.name == "__del__":
                    #check if are not two destructors
                    if self.destructor != None:
                        Base.RaiseException(node, "Only one destructor is allowed")
                    parser = ParserClass.Redirection[ast.FunctionDef](node, self)
                    self.destructor = parser
                else:
                    parser = ParserClass.Redirection[ast.FunctionDef](node, self)
                    self.methods.append(parser)
                parser.Compile()
                if Base.DEBUG:
                    parser.PrintVariables()
                    print('#'*20)
            else:
                Base.RaiseException(node, "This line is not allowed")
        #check if constructor exist
        if self.constructor == None:
            Base.RaiseException(self.nodeAST, "The constructor must exist")
        #check if destructor exist
        if self.destructor == None:
            Base.RaiseException(self.nodeAST, "The destructor must exist")
        return
    
    def PrintVariables(self) -> None:
        print("Class name: " + self.name)
        print("Inheritance: " + str(self.inheritance))
        print("Attributes: " + str(self.attributes))
        print("Methods: " + str(self.methods))
        print("Constructor: " + str(self.constructor))
        print("Destructor: " + str(self.destructor))
        return
            
    
    def GetContent(self) -> str:
        content  = ContentC()
        #H file
        content.H_file += "typedef struct "+self.name+"\n{\n"
        content.H_file +="\n\t//Attributs\n"
        for attribute in self.attributes:
            content.H_file +="\t"+Base.GetType(attribute.type,attribute.nodeAST)+" "+attribute.name+";\n"            
        content.H_file +="\n\t//Methodes\n"
        content.H_file += "\tvoid (*__init__)(struct "+self.name+"*);\n"
        content.H_file += "\tvoid (*__del__)(struct "+self.name+"*);\n"
        for method in self.methods:
            content.H_file += "\t"+Base.GetType(method.return_type, method.nodeAST)+" (*"+method.name+")("
            for index,parameter in enumerate(method.parameters):
                content.H_file += Base.GetType(parameter.type, parameter.nodeAST)+" "+parameter.name
                if index != len(method.parameters)-1:
                    content.H_file += ", "
            content.H_file += ");\n"
        content.H_file +="} "+self.name+";\n"
        content.H_file += Base.GetType(self.name, self.nodeAST)+" "+self.name+"__new__("+self.name+"* self);\n"
        #Top H file
        content.topH_file += "typedef struct "+self.name+" "+self.name+";\n"
        #C file
        content.C_file += Base.GetType(self.name, self.nodeAST)+" "+self.name+"__new__()\n{\n"
        content.C_file += "\t"+Base.GetType(self.name, self.nodeAST)+" self = ("+Base.GetType(self.name, self.nodeAST)+")malloc(sizeof("+self.name+"));\n"
        #set attributes to default value
        for attribute in self.attributes:
            if attribute.value != None:
                content.C_file += "\tself->"+attribute.name+" = ("+Base.GetType(attribute.type,attribute.nodeAST)+")" +\
                    Base.GetValue(attribute.value)+";\n"
        #set methods
        for method in self.methods:
            content.C_file += "\tself->"+method.name+" = "+self.name+"__"+method.name+";\n"
        #set constructor and destructor
        content.C_file += "\tself->__init__ = "+self.name+"__init__;\n"
        content.C_file += "\tself->__del__ = "+self.name+"__del__;\n"
        #call constructor
        content.C_file += "\tself->__init__(self);\n"
        content.C_file += "\treturn self;\n}\n"

        content.C_file += "\n\n"
        content.H_file += "\n\n"
        #add Content of methods
        for method in self.methods:
            content += method.GetContent()
        #add Content of constructor
        content += self.constructor.GetContent()
        #add Content of destructor
        content += self.destructor.GetContent()
        return content
