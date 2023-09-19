from Particle.Modules.Includes import *
from Particle.OverwriteObject.Object import Object
from Particle.EnvironmentSystem import *

@OverwriteObject()
class Component(Object):
    def __init__(self,gameObject, UUID=None,*args, **kwargs):
        super().__init__(UUID,*args, **kwargs)
        self.ComponentName = self.__class__.__name__
        self.gameObject = gameObject