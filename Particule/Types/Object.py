from Particule.Modules.Includes import *

class Object:
    Objects = {}
    def __init__(self, UUID=None):
        self.Particule = GlobalVars.Particule
        if UUID is None:
            UUID = str(uuid.uuid4())
        self.UUID = UUID
        self.Objects[self.UUID] = self
        #print("Object created : " + self.UUID)
        #print(self.Objects)

    @staticmethod
    def GetObject(UUID):
        if UUID is None:
            return None
        return Object.Objects.get(UUID, None)

    def getDict(self):
        return {"UUID": self.UUID}
    
    def setDict(self, dic):
        pass#Override this method to set your own variables
        #On ne doit pas set le UUID, car il doit être set au moment de la création de l'objet

    def Destroy(self):
        self.CallBackDestroy()

    def CallBackDestroy(self):
        #print("Object deleted : " + self.UUID)
        del self.Objects[self.UUID]
        #print(self.Objects)