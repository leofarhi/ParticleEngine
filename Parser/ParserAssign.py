import ast
import Parser.Base as Base
from Parser.Contents.ContentC import ContentC
from Parser.Base import GetAllowedHeader, Header_allowed


class ParserAssign(Base.BaseParser):
    def __init__(self, nodeAST, body):
        super().__init__(nodeAST)
        self.nodeAST = nodeAST
        self.body = body

    def Compile(self) -> None:
        pass