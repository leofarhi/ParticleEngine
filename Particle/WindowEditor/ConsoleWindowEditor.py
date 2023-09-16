from Particle.Modules.Includes import *
from Particle.WindowEditor.WindowEditor import WindowEditor
from Particle.Modules.LanguageSystem import LanguageSystem
from Particle.Modules.Directory import *
from Particle.Modules.Screen import GetScreenSize


class ConsoleWindowEditor(WindowEditor):
    def __init__(self, master=None):
        super().__init__(master,"Console")