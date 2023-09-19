from Base import *
import javalang

class NodeClassDeclaration(BaseNode):
    def __init__(self,nodeAST) -> None:
        super().__init__(nodeAST)
        self.name = ""
        self.methods = []
        self.attributes = []
        self.extends = [] # is list of inherited classes
        self.implements = [] # is list of implemented interfaces
        self.annotations = []  # is list of annotations
        self.access = "private" # is public, private, protected, default is private
    
    def Compile(self) -> None:
        self.name = self.tree.name
        if self.tree.extends is not None:
            for i in self.tree.extends:
                self.extends.append(i[1].name)
        if len(self.extends) > 1:
            RaiseException(self.tree, "Multiple inheritance is not supported")
        if self.tree.implements is not None:
            for i in self.tree.implements:
                self.implements.append(i.name)
        if self.tree.annotations is not None:
            for i in self.tree.annotations:
                self.annotations.append(BaseNode.NewNode("NodeAnnotation")(i))
                self.annotations[-1].Compile()
        if self.tree.modifiers is not None:
            for i in self.tree.modifiers:
                if i == "public" or i == "private" or i == "protected":
                    self.access = i
                else:
                    RaiseException(self.tree, "Unknown modifier: " + i)
        for i in self.tree.constructors:
            self.methods.append(BaseNode.NewNode("NodeMethodDeclaration")(i, True))
            self.methods[-1].Compile()
        for i in self.tree.methods:
            self.methods.append(BaseNode.NewNode("NodeMethodDeclaration")(i))
            self.methods[-1].Compile()
        for i in self.tree.fields:
            self.attributes.append(BaseNode.NewNode("NodeAttributeDeclaration")(i))
            self.attributes[-1].Compile()
        self.PrintVariables()
    
    def PrintVariables(self) -> None:
        print("#" * 20)
        print("Class: " + self.name)
        print("Access: " + self.access)
        print("Extends: " + str(self.extends))
        print("Implements: " + str(self.implements))
        print("Annotations: " + str(self.annotations))
        print("Methods: ")
        for i in self.methods:
            i.PrintVariables()
        print("Attributes: ")
        for i in self.attributes:
            i.PrintVariables()
        print("#" * 20)
        return