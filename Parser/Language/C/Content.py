class Content:
    def __init__(self) -> None:
        self.filename = ""
        self.C_file = ""
        self.H_file = ""

        self.includes = ""

        self.topC_file = ""
        self.topH_file = ""

    #override += operator
    def __iadd__(self, other):
        self.C_file += other.C_file
        self.H_file += other.H_file
        self.includes += other.includes
        self.topC_file += other.topC_file
        self.topH_file += other.topH_file
        return self
    
    #override +
    def __add__(self, other):
        content = Content()
        content.C_file = self.C_file + other.C_file
        content.H_file = self.H_file + other.H_file
        content.includes = self.includes + other.includes
        content.topC_file = self.topC_file + other.topC_file
        content.topH_file = self.topH_file + other.topH_file
        return content
    
    def GetHFile(self) -> str:
        main = "#ifndef "+self.filename.upper()+"_H\n"
        main += "#define "+self.filename.upper()+"_H\n"
        main += self.includes + "\n" + self.topH_file + "\n" + self.H_file + "\n"
        main += "#endif\n"
        return main
    
    def GetCFile(self) -> str:
        main = "#include \""+self.filename+".h\"\n"
        main += self.includes + "\n" + self.topC_file + "\n" + self.C_file + "\n"
        return main