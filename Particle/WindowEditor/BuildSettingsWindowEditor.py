from Particle.Modules.Includes import *
from Particle.WindowEditor.WindowEditor import WindowEditor
from Particle.Modules.LanguageSystem import LanguageSystem
from Particle.Modules.Directory import *
from Particle.Modules.Screen import GetScreenSize

class BuildSettingsWindowEditor(WindowEditor):
    def __init__(self, master=None):
        super().__init__(master,"BuildSettings")

    @AddCallBackToStack("OnCreateMenu", 3)
    def OnCreateMenu():
        GlobalVars.Particle.AddCommandsMenu("File", {
            "Parameters de compilation": (),
            "Compiler": (),
        }, True)