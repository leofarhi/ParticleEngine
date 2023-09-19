from Base import *

class NodeAnnotation(BaseNode):
    def __init__(self,nodeAST) -> None:
        super().__init__(nodeAST)
        self.name = ""
        self.argument = None

    def Compile(self) -> None:
        self.name = self.tree.name
        if self.tree.element is not None:
            #check if is literal
            if type(self.tree.element) == javalang.tree.Literal:
                self.argument = self.tree.element.value
            else:
                raise Exception("Unknown annotation element type")