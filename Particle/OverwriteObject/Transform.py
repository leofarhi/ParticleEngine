
from Particle.Modules.Includes import *
from Particle.OverwriteObject.Object import Object
from Particle.OverwriteObject.Component import Component
from Particle.EnvironmentSystem import *

@OverwriteObject()
class Transform(Component):
    def __init__(self,gameObject, UUID=None,*args, **kwargs):
        super().__init__(gameObject,UUID=UUID,*args, **kwargs)
        self.children = []
        self.parent = None
        
    def SetParent(self, parent):
        if self.parent != None:
            self.parent.children.remove(self)
        self.parent = parent
        if parent != None:
            parent.children.append(self)
        Hierarchy = GlobalVars.Particle.GetEditor("Hierarchy")
        if Hierarchy != None:
            Hierarchy.UpdateHierarchy(self.gameObject)