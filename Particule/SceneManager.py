
from Particule.Modules.Includes import *
from Particule.Modules.Includes import ctk
from Particule.Modules.LanguageSystem import LanguageSystem
from Particule.Modules.Directory import *
from Particule.WindowEditor.WindowEditor import WindowEditor
from Particule.Types.AssetItem import AssetItem

class SceneManager:
    def __init__(self,_Particule):
        self.Particule = _Particule
        self.CurrentScene = None


    def LoadScene(self,assetItem):
        pass

    def UnloadScene(self):
        pass