from Particule.Modules.Includes import *
from Particule.WindowEditor.WindowEditor import WindowEditor
from Particule.Modules.LanguageSystem import LanguageSystem
from Particule.Modules.Directory import *
from Particule.Modules.Screen import GetScreenSize

class BuildSettingsWindowEditor(WindowEditor):
    def __init__(self, master=None):
        super().__init__(master,"BuildSettings")

    @AddCallBackToStack("OnCreateMenu", 3)
    def OnCreateMenu():
        GlobalVars.Particule.AddCommandsMenu("File", {
            "Parameters de compilation": (),
            "Compiler": (),
        }, True)