from Base import *

class NodeMethodDeclaration(BaseNode):
    def __init__(self,nodeAST,isConstructor=False) -> None:
        super().__init__(nodeAST)
        self.name = ""
        self.parameters = []
        self.returnType = ""
        self.annotations = []
        self.access = "private"
        self.isStatic = False
        self.isConstructor = isConstructor

    def Compile(self) -> None:
        self.name = self.tree.name
        if not self.isConstructor:
            if self.tree.return_type is not None:
                self.returnType = self.tree.return_type.name
            else:
                self.returnType = "void"
        """
        if self.tree.parameters is not None:
            for i in self.tree.parameters:
                self.parameters.append(BaseNode.NewNode("NodeParameter")(i))
                self.parameters[-1].Compile()
        """
        if self.tree.annotations is not None:
            for i in self.tree.annotations:
                self.annotations.append(i.name)
        if self.tree.modifiers is not None:
            for i in self.tree.modifiers:
                if i == "public" or i == "private" or i == "protected":
                    self.access = i
                elif i == "static":
                    self.isStatic = True
                else:
                    RaiseException(self.tree, "Unknown modifier: " + i)
        self.PrintVariables()

    def PrintVariables(self) -> None:
        print("£" * 20)
        print("Method: " + self.name)
        print("Constructor: " + str(self.isConstructor))
        print("Access: " + self.access)
        print("Static: " + str(self.isStatic))
        print("Return Type: " + self.returnType)
        print("Parameters: " + str(self.parameters))
        print("Annotations: " + str(self.annotations))
        print("£" * 20)
        return