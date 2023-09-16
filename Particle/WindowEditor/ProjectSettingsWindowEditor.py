from Particle.Modules.Includes import *
from Particle.WindowEditor.WindowEditor import WindowEditor
from Particle.Modules.LanguageSystem import LanguageSystem
from Particle.Modules.Directory import *
from Particle.Modules.Screen import GetScreenSize

class ProjectSettingsWindowEditor(WindowEditor):
    def __init__(self, master=None):
        super().__init__(master,"ProjectSettings")

    @AddCallBackToStack("OnCreateMenu", 9)
    def OnCreateMenu():
        GlobalVars.Particle.AddCommandsMenu("Edit", {
            "Paramètres du projet": (),
        }, True)