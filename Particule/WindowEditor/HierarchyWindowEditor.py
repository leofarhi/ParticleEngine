from Particule.Modules.Includes import *
from Particule.WindowEditor.WindowEditor import WindowEditor
from Particule.Modules.LanguageSystem import LanguageSystem
from Particule.Modules.Directory import *
from Particule.Modules.Screen import GetScreenSize


class HierarchyWindowEditor(WindowEditor):
    def __init__(self, master=None):
        super().__init__(master,"Hierarchy")