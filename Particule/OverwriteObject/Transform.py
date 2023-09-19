
from Particule.Modules.Includes import *
from Particule.OverwriteObject.Object import Object
from Particule.OverwriteObject.Component import Component
from Particule.EnvironmentSystem import *

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
        Hierarchy = GlobalVars.Particule.GetEditor("Hierarchy")
        if Hierarchy != None:
            Hierarchy.UpdateHierarchy(self.gameObject)