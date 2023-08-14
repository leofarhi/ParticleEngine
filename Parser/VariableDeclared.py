class VariableDeclared:
    def __init__(self, nodeAST, name, type, value=None):
        self.nodeAST = nodeAST
        self.name = name
        self.value = value
        self.type = type
        self.static = False
        self.visibility = "private"
        self.UI_visibility = False
        