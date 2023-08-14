from Particule.Modules.Includes import *

class SpecialImage:
    def __init__(self, path):
        self.path = path
        self.image = None
        self.imageTk = None
        self.size = None
        self.LoadImage()

    def LoadImage(self):
        self.image = Image.open(self.path)
        self.size = self.image.size
        self.imageTk = ImageTk.PhotoImage(self.image)