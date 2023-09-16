
from Particle.Modules.Includes import *
from Particle.Modules.Includes import ctk
from Particle.Modules.LanguageSystem import LanguageSystem
from Particle.Modules.Directory import *
from Particle.WindowEditor.WindowEditor import WindowEditor
from Particle.Types.AssetItem import AssetItem
from Particle.Types.Scene import Scene

class SceneManager:
    def __init__(self,_Particle):
        self.Particle = _Particle
        self.CurrentScene = None


    def LoadScene(self,assetItem):
        if self.CurrentScene != None:
            self.UnloadScene()
        self.CurrentScene = Scene(assetItem=assetItem)
        self.CurrentScene.Load()
        self.Particle.GetEditor("Hierarchy").Update()
        #print("Scene Loaded")

    def UnloadScene(self):
        if self.CurrentScene == None:
            return
        self.CurrentScene.Unload()
        self.Particle.GetEditor("Hierarchy").Update()
        #print("Scene Unloaded")

    def CreateScene(self,path):
        self.CurrentScene = Scene()
        self.CurrentScene.Save(path)
        asset = AssetItem.create(path)
        self.CurrentScene.assetItem = asset
        self.Particle.GetEditor("Project").Update()
        self.Particle.GetEditor("Hierarchy").Update()
        #print("Scene Created")