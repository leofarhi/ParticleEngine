from Particule.Modules.Includes import *
from Particule.Types.Object import Object

class Component(Object):
    def __init__(self,gameObject, UUID=None):
        super().__init__(UUID)
        self.gameObject = gameObject

    def getDict(self):
        dict = super().getDict()
        dict["gameObject"] = self.gameObject.UUID
        dict["__name__"] = self.__class__.__name__
        return dict
    
    def setDict(self, dict):
        self.gameObject = self.GetObject(dict.get("gameObject", None))