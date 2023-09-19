from Base import *
import javalang
import os, sys

class NodeFile(BaseNode):
    def __init__(self,path,tree) -> None:
        super().__init__(tree)
        self.path = path
        self.package = None
        self.imports = []
        self.body = []

    def Compile(self) -> None:
        if self.tree.package is not None:
            self.package = self.tree.package.name
        for i in self.tree.imports:
            self.imports.append(i.path)
        for i in self.tree.types:
            if isinstance(i, javalang.tree.ClassDeclaration):
                self.body.append(BaseNode.NewNode("NodeClassDeclaration")(i))
                self.body[-1].Compile()
            elif isinstance(i, javalang.tree.EnumDeclaration):
                self.body.append(BaseNode.NewNode("NodeEnumDeclaration")(i))
                self.body[-1].Compile()
            else:
                RaiseException(i, "Unknown node type: " + str(type(i)))
        self.PrintVariables()
    
    def PrintVariables(self) -> None:
        print("#" * 20)
        print("Package: " + str(self.package))
        print("Imports: " + str(self.imports))
        print("Classes: ")
        for i in self.body:
            i.PrintVariables()
        print("#" * 20)
        return
        