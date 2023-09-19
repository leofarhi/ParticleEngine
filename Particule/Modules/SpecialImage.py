from Particule.Modules.Includes import *
import PIL.Image

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

    def Resize(self, width, height):
        self.size = (width, height)
        #resize image keeping alpha
        self.image = self.image.convert("RGBA").resize(self.size, PIL.Image.LANCZOS)
        self.imageTk = ImageTk.PhotoImage(self.image)
        return self