from Particule.Modules.Includes import *
from Particule.Types.Object import Object

class Component(Object):
    def __init__(self,gameObject, name, UUID=None):
        super().__init__(name, UUID)
        self.gameObject = gameObject