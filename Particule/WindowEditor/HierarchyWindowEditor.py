from Particule.Modules.Includes import *
from Particule.WindowEditor.WindowEditor import WindowEditor
from Particule.Modules.LanguageSystem import LanguageSystem
from Particule.Modules.Directory import *
from Particule.Modules.Screen import GetScreenSize
from Particule.Modules.SpecialImage import SpecialImage


class HierarchyWindowEditor(WindowEditor):
    def __init__(self, master=None):
        super().__init__(master,"Hierarchy")

        self.hierarchyTreeScrollbar = ctk.CTkScrollbar(self.window,orientation="vertical")
        self.hierarchyTree = MyTreeview(self.window, columns=("UUID","Type"), 
                                      selectmode="browse", show="tree",
                                        displaycolumns=(),
                                        yscrollcommand=self.hierarchyTreeScrollbar.set)
        self.hierarchyTreeScrollbar.configure(command=self.hierarchyTree.yview)

        self.gameobjectIcon = SpecialImage("lib/UI/Icons/Project/folder_small.png").imageTk
        self.PrefabIcon = SpecialImage("lib/UI/Icons/Project/textfile_small.png").imageTk
        self.SceneIcon = SpecialImage("lib/UI/Icons/Project/textfile_small.png").imageTk
        
        self.hierarchyTree.pack(side=LEFT, fill=BOTH, expand=True)
        self.hierarchyTreeScrollbar.pack(side=LEFT, fill=Y)

    def Update(self):
        #clear tree
        self.hierarchyTree.delete(*self.hierarchyTree.get_children())
        scene = self.Particule.sceneManager.CurrentScene
        if scene == None:
            return
        if scene.assetItem == None:
            return
        #add root
        self.hierarchyTree.insert("", 0, scene.name, text=scene.name, values=(scene.UUID, "scene"), tags=("scene"), image=self.SceneIcon)