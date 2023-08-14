from Particule.Modules.Includes import *
from Particule.Types.Object import Object

class Scene(Object):
    def __init__(self, name, UUID=None):
        super().__init__(name, UUID)
        self.gameObjects = {}
