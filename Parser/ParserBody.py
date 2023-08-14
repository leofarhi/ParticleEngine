import ast
import Parser.Base as Base
from Parser.Contents.ContentC import ContentC
from Parser.Base import GetAllowedHeader, Header_allowed
from Parser.ParserAssign import ParserAssign


class ParserBody(Base.BaseParser):
    def __init__(self, ParserParent,body):
        super().__init__(ParserParent.nodeAST)
        self.nodeAST = ParserParent.nodeAST
        self.ParserParent = ParserParent
        self.body = body
        self.variablesDeclaration = [] #{nodeAST, name, type, value, static}

    def GetVariable(self, name):
        for variable in self.variablesDeclaration:
            if variable.name == name:
                return variable
        return None

    def Compile(self) -> None:
        for node in self.body:
            if isinstance(node, ast.Pass):
                continue
            elif isinstance(node, ast.Assign):
                pass#self.variablesDeclaration.append(self.CompileAssign(node))
            else:
                Base.RaiseException(node, "This line is not allowed")