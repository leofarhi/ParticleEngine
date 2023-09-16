from Particle.Modules.Includes import *
from Particle.Types.Object import Object
from Particle.Types.Tag import Tag
from Particle.Types.Layer import Layer
from Particle.Types.Component import Component


class GameObject(Object):
    def __init__(self, name, UUID=None):
        super().__init__(UUID)
        self.name = name
        self.activeInHierarchy = True
        self.activeSelf = True
        self.isStatic = False
        self.layer = Layer.Default
        #self.scene = scene
        self.tag = Tag.Untagged
        #self.transform = Transform(self)
        self.components = []#[self.transform]

        self.frameOfComponents = None #la frame qui affiche les components dans l'Inspector

    def getDict(self):
        dict = super().getDict()
        dict["name"] = self.name
        dict["activeInHierarchy"] = self.activeInHierarchy
        dict["activeSelf"] = self.activeSelf
        dict["isStatic"] = self.isStatic
        dict["layer"] = self.layer
        dict["tag"] = self.tag
        dict["components"] = [component.getDict() for component in self.components]
        return dict
    
    def setDict(self, dict):
        super().setDict(dict)
        self.name = dict.get("name", self.name)
        self.activeInHierarchy = dict.get("activeInHierarchy", self.activeInHierarchy)
        self.activeSelf = dict.get("activeSelf", self.activeSelf)
        self.isStatic = dict.get("isStatic", self.isStatic)
        self.layer = dict.get("layer", self.layer)
        self.tag = dict.get("tag", self.tag)
        print("TODO: GameObject setDict")
        #self.components = [Component.getFromDict(component) for component in dict["components"]]