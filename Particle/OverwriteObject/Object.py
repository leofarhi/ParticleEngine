from Particle.Modules.Includes import *
from Particle.EnvironmentSystem import *

@OverwriteObject()
class Object(InstanceEnvironmentObject):
    Objects = {}
    def __init__(self, UUID=None,*args, **kwargs):
        InstanceEnvironmentObject.__init__(self,*args, **kwargs)
        self.Particle = GlobalVars.Particle
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

    def __reference__(self):
        return self.UUID
    
    def __setreference__(data):
        return Object.GetObject(data)

    def Destroy(self):
        super().Destroy()
        self.CallBackDestroy()

    def CallBackDestroy(self):
        del self.Objects[self.UUID]