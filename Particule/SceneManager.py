
from Particule.Modules.Includes import *
from Particule.Modules.Includes import ctk
from Particule.Modules.LanguageSystem import LanguageSystem
from Particule.Modules.Directory import *
from Particule.WindowEditor.WindowEditor import WindowEditor
from Particule.Types.AssetItem import AssetItem
from Particule.Types.Scene import Scene

class SceneManager:
    def __init__(self,_Particule):
        self.Particule = _Particule
        self.CurrentScene = None


    def LoadScene(self,assetItem):
        if self.CurrentScene != None:
            self.UnloadScene()
        self.CurrentScene = Scene(assetItem=assetItem)
        self.CurrentScene.Load()
        self.Particule.GetEditor("Hierarchy").Update()
        #print("Scene Loaded")

    def UnloadScene(self):
        if self.CurrentScene == None:
            return
        self.CurrentScene.Unload()
        self.Particule.GetEditor("Hierarchy").Update()
        #print("Scene Unloaded")

    def CreateScene(self,path):
        self.CurrentScene = Scene()
        self.CurrentScene.Save(path)
        asset = AssetItem.create(path)
        self.CurrentScene.assetItem = asset
        self.Particule.GetEditor("Project").Update()
        self.Particule.GetEditor("Hierarchy").Update()
        #print("Scene Created")