from Base import *

class NodeType(BaseNode):
    def __init__(self,nodeAST) -> None:
        super().__init__(nodeAST)
        self.name = ""
        self.isArray = 0 #if 0 then not array, if 1 then array, if 2 then array of arrays etc...
        self.arguments = []


    def Compile(self) -> None:
        self.name = self.tree.name
        if "arguments" in self.tree.attrs and type(self.tree.arguments) == list:
            CLASS = BaseNode.NewNode("NodeType")
            self.arguments = [CLASS(i.type) for i in self.tree.arguments]
            for i in self.arguments:
                i.Compile()
        if "dimensions" in self.tree.attrs and type(self.tree.dimensions) == list:
            self.isArray = len(self.tree.dimensions)

    def __str__(self) -> str:
        return self.name