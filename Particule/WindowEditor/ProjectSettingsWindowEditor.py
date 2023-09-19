from Particule.Modules.Includes import *
from Particule.WindowEditor.WindowEditor import WindowEditor
from Particule.Modules.LanguageSystem import LanguageSystem
from Particule.Modules.Directory import *
from Particule.Modules.Screen import GetScreenSize

class ProjectSettingsWindowEditor(WindowEditor):
    def __init__(self, master=None):
        super().__init__(master,"ProjectSettings")

    @AddCallBackToStack("OnCreateMenu", 9)
    def OnCreateMenu():
        GlobalVars.Particule.AddCommandsMenu("Edit", {
            "Paramètres du projet": (),
        }, True)