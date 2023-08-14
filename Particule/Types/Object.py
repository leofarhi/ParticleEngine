from Particule.Modules.Includes import *

class Object:
    def __init__(self, name, UUID=None):
        self.Particule = GlobalVars.Particule
        self.name = name
        if UUID is None:
            UUID = str(uuid.uuid4())
        self.UUID = UUID