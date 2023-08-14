from Particule.Modules.Includes import *
from Particule.Types.Object import Object
from Particule.Types.Tag import Tag
from Particule.Types.Layer import Layer
from Particule.Types.Component import Component


class GameObject(Object):
    def __init__(self, name, UUID=None):
        super().__init__(name, UUID)
        self.activeInHierarchy = True
        self.activeSelf = True
        self.isStatic = False
        self.layer = Layer.Default
        #self.scene = scene
        self.tag = Tag.Untagged
        #self.transform = Transform(self)
        self.components = []#[self.transform]

        self.frameOfComponents = None #la frame qui affiche les components dans l'Inspector