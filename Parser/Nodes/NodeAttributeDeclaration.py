from Base import *

class NodeAttributeDeclaration(BaseNode):
    def __init__(self,nodeAST) -> None:
        super().__init__(nodeAST)
        self.name = ""
        self.type = ""
        self.access = "private"
        self.isStatic = False
        self.defaultValue = None
        self.annotations = []
    
    def Compile(self) -> None:
        self.name = self.tree.declarators[0].name
        self.type = self.tree.type.name
        if self.tree.modifiers is not None:
            for i in self.tree.modifiers:
                if i == "public" or i == "private" or i == "protected":
                    self.access = i
                elif i == "static":
                    self.isStatic = True
                else:
                    RaiseException(self.tree, "Unknown modifier: " + i)
        if self.tree.declarators[0].initializer is not None:
            self.defaultValue = self.tree.declarators[0].initializer.value
        if self.tree.annotations is not None:
            for i in self.tree.annotations:
                self.annotations.append(i.name)
        self.PrintVariables()

    def PrintVariables(self) -> None:
        print("-" * 20)
        print("Attribute: " + self.name)
        print("Access: " + self.access)
        print("Static: " + str(self.isStatic))
        print("Type: " + self.type)
        print("Default Value: " + str(self.defaultValue))
        print("Annotations: " + str(self.annotations))
        print("-" * 20)
        return