import ast
import Parser.Base as Base
from Parser.Contents.ContentC import ContentC
from Parser.Base import GetAllowedHeader, Header_allowed
import Parser.ParserBody as ParserBody
from Parser.VariableDeclared import VariableDeclared


class ParserFunction(Base.BaseParser):
    Register = []
    def __init__(self, nodeAST, methodOf=None):
        super().__init__(nodeAST)
        self.name = ""
        self.nodeAST = nodeAST
        self.return_type = None
        self.parameters = [] #list of VariableDeclared
        self.body = None #nodeAST
        self.visibility = "private"
        self.static = False
        self.override = False
        self.virtual = False
        self.methodOf = methodOf #if None, it's a function, else it's a method of a class
        ParserFunction.Register.append(self)

    def Compile(self) -> None:
        if not isinstance(self.nodeAST, ast.FunctionDef):
            Base.RaiseException(self.nodeAST, "The nodeAST must be a FunctionDef")
        self.name = self.nodeAST.name
        #check if name start with __
        if self.name.startswith("__"):
            if self.methodOf == None:
                Base.RaiseException(self.nodeAST, "The function name must not start with __")
            elif not self.name in ["__init__", "__del__"]:
                Base.RaiseException(self.nodeAST, "The method name must not start with __")
        if self.methodOf == None and "__" in self.name:
            base = self.name.split("__",1)[0]
            if ParserFunction.Redirection[ast.ClassDef].GetClassByName(base) != None:
                Base.RaiseException(self.nodeAST, "The function name must not start with "+base+"__")
        #check in register if already exist
        for parserFunction in ParserFunction.Register:
            if parserFunction.name == self.name and parserFunction != self and parserFunction.methodOf == self.methodOf:
                Base.RaiseException(self.nodeAST, "The function name already exist")
        #check return type
        if self.nodeAST.returns != None:
            self.return_type = self.nodeAST.returns.id
        
        if self.methodOf != None:
            if self.name in ["__init__", "__del__"] and self.return_type != None:
                Base.RaiseException(self.nodeAST, "This method must not have a return type")
            if self.name == "__del__":
                if len(self.nodeAST.args.args) != 1:
                    Base.RaiseException(self.nodeAST, "The destructor must have only one parameter")
        #check parameters
        if self.methodOf != None:
            if len(self.nodeAST.args.args) == 0:
                    Base.RaiseException(self.nodeAST, "The constructor must have at least one parameter")
            if self.nodeAST.args.args[0].arg != "self":
                Base.RaiseException(self.nodeAST, "The first parameter of the method must be self")
        for index,node in enumerate(self.nodeAST.args.args):
            if not isinstance(node, ast.arg):
                Base.RaiseException(node, "The parameter must be an arg")
            if self.methodOf != None and node.arg == "self" and index == 0:
                continue
            if node.annotation == None:
                Base.RaiseException(node, "The parameter must have a type")
            self.parameters.append(VariableDeclared(node, node.arg, node.annotation.id, None))
        #check body
        if self.nodeAST.body == None:
            Base.RaiseException(self.nodeAST, "The function must have a body")
        parserBody = ParserBody.ParserBody(self,self.nodeAST.body)
        self.body = parserBody
        parserBody.Compile()
        #check header
        Header_settings = {"visibility": "private", "static": False, "override": False, "virtual": False}
        for node in self.nodeAST.decorator_list:
            if isinstance(node, ast.Name):
                if node.id in GetAllowedHeader():
                    if node.id in Header_allowed["visibilities"]:
                        Header_settings["visibility"] = node.id
                    elif node.id in Header_allowed["static"]:
                        Header_settings["static"] = True
                    elif node.id in Header_allowed["override"]:
                        Header_settings["override"] = True
                    elif node.id in Header_allowed["virtual"]:
                        Header_settings["virtual"] = True
                else:
                    Base.RaiseException(node, "Header not allowed")
            else:
                Base.RaiseException(node, "The header must be a string")
        self.visibility = Header_settings["visibility"]
        self.static = Header_settings["static"]
        self.override = Header_settings["override"]
        self.virtual = Header_settings["virtual"]
        return
            
    def GetContent(self) -> str:
        content = ContentC()
        content.H_file += Base.GetType(self.return_type, self.nodeAST)+" "
        if self.methodOf != None:
            content.H_file += self.methodOf.name
            if not self.name.startswith("__"):
                content.H_file += "__"
        content.H_file += self.name + "("
        if self.methodOf != None:
            content.H_file += Base.GetType(self.methodOf.name, self.nodeAST)+" self"
            if len(self.parameters) > 0:
                content.H_file += ", "
        for index,parameter in enumerate(self.parameters):
            content.H_file += Base.GetType(parameter.type, parameter.nodeAST)+" "+parameter.name
            if index != len(self.parameters)-1:
                content.H_file += ", "
        content.H_file += ");\n"
        content.C_file += Base.GetType(self.return_type, self.nodeAST)+" "
        if self.methodOf != None:
            content.C_file += self.methodOf.name
            if not self.name.startswith("__"):
                content.C_file += "__"
        content.C_file += self.name + "("
        if self.methodOf != None:
            content.C_file += Base.GetType(self.methodOf.name, self.nodeAST)+" self"
            if len(self.parameters) != 0:
                content.C_file += ", "
        for index,parameter in enumerate(self.parameters):
            content.C_file += Base.GetType(parameter.type, parameter.nodeAST)+" "+parameter.name
            if index != len(self.parameters)-1:
                content.C_file += ", "
        content.C_file += ")\n{\n"
        content.C_file += "\t//TODO\n"
        content.C_file += "}\n"
        return content
    
    def PrintVariables(self) -> None:
        print("name: " + self.name)
        print("return_type: " + str(self.return_type))
        print("parameters: " + str(self.parameters))
        print("body: " + str(self.body))
        print("visibility: " + self.visibility)
        print("static: " + str(self.static))
        print("override: " + str(self.override))
        print("virtual: " + str(self.virtual))
        print("methodOf: " + str(self.methodOf))
        return