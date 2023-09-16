from Particle.Modules.Includes import *
from Particle.WindowEditor.WindowEditor import WindowEditor
from Particle.Modules.LanguageSystem import LanguageSystem
from Particle.Modules.Directory import *
from Particle.Modules.Screen import GetScreenSize

class PreferencesWindowEditor(WindowEditor):
    def __init__(self, master=None):
        super().__init__(master,"Preferences")

    @AddCallBackToStack("OnCreateMenu", 10)
    def OnCreateMenu():
        GlobalVars.Particle.AddCommandsMenu("Edit", {
            "Préférences": ()
        }, False)