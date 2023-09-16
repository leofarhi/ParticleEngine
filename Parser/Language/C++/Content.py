class Content:
    def __init__(self) -> None:
        self.filename = ""
        self.Cpp_file = ""
        self.Hpp_file = ""

        self.includes = ""

        self.topCpp_file = ""
        self.topHpp_file = ""

    #override += operator
    def __iadd__(self, other):
        self.Cpp_file += other.Cpp_file
        self.Hpp_file += other.Hpp_file
        self.includes += other.includes
        self.topCpp_file += other.topCpp_file
        self.topHpp_file += other.topHpp_file
        return self
    
    #override +
    def __add__(self, other):
        content = Content()
        content.Cpp_file = self.Cpp_file + other.Cpp_file
        content.Hpp_file = self.Hpp_file + other.Hpp_file
        content.includes = self.includes + other.includes
        content.topCpp_file = self.topCpp_file + other.topCpp_file
        content.topHpp_file = self.topHpp_file + other.topHpp_file
        return content
    
    def GetHppFile(self) -> str:
        main = "#ifndef "+self.filename.upper()+"_H\n"
        main += "#define "+self.filename.upper()+"_H\n"
        main += self.includes + "\n" + self.topHpp_file + "\n" + self.Hpp_file + "\n"
        main += "#endif\n"
        return main
    
    def GetCppFile(self) -> str:
        main = "#include \""+self.filename+".h\"\n"
        main += self.includes + "\n" + self.topCpp_file + "\n" + self.Cpp_file + "\n"
        return main