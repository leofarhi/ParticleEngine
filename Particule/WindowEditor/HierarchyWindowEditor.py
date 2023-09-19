from Particule.Modules.Includes import *
from Particule.WindowEditor.WindowEditor import WindowEditor
from Particule.Modules.LanguageSystem import LanguageSystem
from Particule.Modules.Directory import *
from Particule.Modules.Screen import GetScreenSize
from Particule.Modules.SpecialImage import SpecialImage
from Particule.OverwriteObject.Object import Object
from Particule.OverwriteObject.Scene import Scene


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
        self.__selectedItems = []

        #bind
        #left click
        self.hierarchyTree.bind("<ButtonRelease-1>", self.OnClick)

    def OnClick(self,event):
        #get item
        slc = self.hierarchyTree.selection()
        if len(slc) == 0:return
        item = slc[0]
        UUID = self.hierarchyTree.item(item,"values")[0]
        __selectedItems = [item]
        if __selectedItems == self.__selectedItems:return
        #get gameObject
        gameObject = Object.GetObject(UUID)
        if gameObject!=None and type(gameObject).__name__ == "GameObject":
            inspector = self.Particule.GetEditor("Inspector")
            if inspector != None:inspector.ShowInspector("GameObject")
            Scene.SetSelectedGameObjects([gameObject])
            self.__selectedItems = [item]


    def RemoveGameObjectInHierarchy(self,gameObject):
        if self.hierarchyTree.exists(gameObject.UUID):
            self.hierarchyTree.delete(gameObject.UUID)
        self.__selectedItems.clear()

    def OpenObject(self,object):
        if object == None:
            return
        if type(object).__name__ in ["Scene","GameObject"]:
            if self.hierarchyTree.exists(object.UUID):
                self.hierarchyTree.item(object.UUID,open=True)

    
    def FocusObject(self,object):
        if object == None:
            return
        if type(object).__name__ in ["Scene","GameObject"]:
            if self.hierarchyTree.exists(object.UUID):
                self.hierarchyTree.focus(object.UUID)
                self.hierarchyTree.selection_set(object.UUID)
                self.hierarchyTree.see(object.UUID)

    def __GetparentUUID(self,gameObject):
        scene = self.Particule.sceneManager.CurrentScene
        parent = gameObject.transform.parent
        position = "end"
        if parent == None:
            parent = scene
            allGameObjectWithoutParent = [i for i in scene.gameObjectsList if i.transform.parent == None]
            position = allGameObjectWithoutParent.index(gameObject)
        else:
            parent = parent.gameObject
            allGameObjectWithParent = [i for i in parent.transform.children]
            position = allGameObjectWithParent.index(gameObject.transform)
        return parent,position

    def UpdateHierarchy(self,gameObjectEdited=None):
        scene = self.Particule.sceneManager.CurrentScene
        if scene == None:
            return
        if scene.assetItem == None:
            return
        if gameObjectEdited == None:
            openedGameObject = []
            #get opened GameObject
            def GetOpenGameObject(item):
                if self.hierarchyTree.item(item,"open") == True:
                    openedGameObject.append(item)
                for i in self.hierarchyTree.get_children(item):
                    GetOpenGameObject(i)
            GetOpenGameObject("")
            #clear tree
            self.hierarchyTree.delete(*self.hierarchyTree.get_children())
            #add root
            self.hierarchyTree.insert("", 0, scene.UUID, text=scene.name, values=(scene.UUID, "scene"), tags=("scene"), image=self.SceneIcon)
            #add children
            for gameObject in scene.gameObjectsList:
                parent,position = self.__GetparentUUID(gameObject)
                self.hierarchyTree.insert(parent.UUID, position, gameObject.UUID, text=gameObject.name, values=(gameObject.UUID, "gameObject"), tags=("gameObject"), image=self.gameobjectIcon)
            #open GameObject
            for gameObject in openedGameObject:
                if self.hierarchyTree.exists(gameObject):
                    self.hierarchyTree.item(gameObject,open=True)
        else:
            #add root if not exists
            if not self.hierarchyTree.exists(scene.UUID):
                self.hierarchyTree.insert("", 0, scene.UUID, text=scene.name, values=(scene.UUID, "scene"), tags=("scene"), image=self.SceneIcon)
            #check if gameObjectEdited.UUID is in the tree
            if self.hierarchyTree.exists(gameObjectEdited.UUID):
                #update gameObjectEdited
                self.hierarchyTree.item(gameObjectEdited.UUID, text=gameObjectEdited.name, values=(gameObjectEdited.UUID, "gameObject"), tags=("gameObject"), image=self.gameobjectIcon)
                #Update parent
                parent,position = self.__GetparentUUID(gameObjectEdited)
                self.hierarchyTree.move(gameObjectEdited.UUID, parent.UUID, position)
            else:
                #add gameObjectEdited
                parent,position = self.__GetparentUUID(gameObjectEdited)
                self.hierarchyTree.insert(parent.UUID, position, gameObjectEdited.UUID, text=gameObjectEdited.name, values=(gameObjectEdited.UUID, "gameObject"), tags=("gameObject"), image=self.gameobjectIcon)