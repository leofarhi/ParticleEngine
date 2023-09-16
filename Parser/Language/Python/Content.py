class Content:
    def __init__(self) -> None:
        self.filename = ""
        self.file = ""
        self.includes = ""
        self.top_file = ""

    #override += operator
    def __iadd__(self, other):
        self.file += other.file
        self.includes += other.includes
        self.top_file += other.top_file
        return self
    
    #override +
    def __add__(self, other):
        content = Content()
        content.file = self.file + other.file
        content.includes = self.includes + other.includes
        content.top_file = self.top_file + other.top_file
        return content
    
    def GetFile(self) -> str:
        main = self.includes + "\n" + self.top_file + "\n" + self._file + "\n"
        return main