import javalang
from Content import Content

class BaseNode:
    RegisterNodes = dict()
    def NewNode(name):
        return BaseNode.RegisterNodes[name]
    def __init__(self,nodeAST) -> None:
        self.tree = nodeAST

    def Compile(self) -> None:
        return
    
    def GetContent(self) -> Content:
        return Content()
    
    def PrintVariables(self) -> None:
        return
    
def RaiseException(node, msg):
    raise Exception(msg + " |#| in line " + str(node.position.line) + " and col " + str(node.position.column))