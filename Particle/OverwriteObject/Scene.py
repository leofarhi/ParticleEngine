from Particle.Modules.Includes import *
from Particle.OverwriteObject.Object import Object
from Particle.OverwriteObject.GameObject import GameObject
from Particle.OverwriteObject.AssetItem import AssetItem
from Particle.EnvironmentSystem import *
from Particle.WindowEditor.InspectorWindowEditor import InspectorWindowEditor

@OverwriteObject()
class Scene(Object):
    def __init__(self, UUID=None, assetItem=None,*args, **kwargs):
        super().__init__(UUID,*args, **kwargs)
        self.gameObjects = {}
        self.assetItem = assetItem

        self.SelectedGameObjects = []
    
    def SetSelectedGameObjects(gameObjects: list):
        self = GlobalVars.Particle.sceneManager.CurrentScene
        if self==None:return
        self.SelectedGameObjects = gameObjects
        CallBacksStackCall("SelectedGameObjectsChanged",self.SelectedGameObjects)

    @property
    def gameObjectsList(self) -> list:
        return list(self.gameObjects.values())
    
    @property
    def name(self) -> str:
        if self.assetItem is None:
            return "New Scene"
        return self.assetItem.name
    
    def AddGameObject(self):
        gameObject = GameObject("New GameObject")
        self.gameObjects[gameObject.UUID] = gameObject
        gameObject.SetScene(self)
        return gameObject

    def Save(self, path=None):
        if path is None:
            if self.assetItem is None:
                raise Exception("No path provided")
            path = self.assetItem.path
        if self.assetItem is None:
            name = os.path.basename(path)
        else:
            name = self.assetItem.name
        listOfGameObjectsDict = []
        listOfComponentsDict = []
        for gameObject in self.gameObjectsList:
            listOfGameObjectsDict.append(gameObject.getDict())
            for component in gameObject.components:
                listOfComponentsDict.append(component.getDict())
        data = {
            "gameObjects": listOfGameObjectsDict,
            "components": listOfComponentsDict,
        }
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def Load(self):
        self.SelectedGameObjects.clear()
        hierarchy = self.Particle.GetEditor("Hierarchy")
        if hierarchy!= None:
            hierarchy.UpdateHierarchy()
            hierarchy.OpenObject(self)
        InspectorWindowEditor.Instance.ShowInspector("")
        if self.assetItem is None:
            raise Exception("No path provided")
        with open(self.assetItem.path, "r", encoding="utf-8") as file:
            data = json.load(file)
        for gameObjectDict in data["gameObjects"]:
            gameObject = GameObject(UUID=gameObjectDict["UUID"])
            gameObject.__TemporaryDict__ = gameObjectDict
            self.gameObjects[gameObject.UUID] = gameObject
        TempComponents = []
        for componentDict in data["components"]:
            component = NewEnv(componentDict["ComponentName"],Object.GetObject(componentDict["gameObject"]),UUID=componentDict["UUID"])
            component.__TemporaryDict__ = componentDict
            TempComponents.append(component)
        for component in TempComponents:
            component.setDict(component.__TemporaryDict__)
            del component.__TemporaryDict__
        for gameObject in self.gameObjectsList:
            gameObject.setDict(gameObject.__TemporaryDict__)
            del gameObject.__TemporaryDict__
        for gameObject in self.gameObjectsList:
            gameObject.SetScene(self)

    def Unload(self):
        self.SelectedGameObjects.clear()
        hierarchy = self.Particle.GetEditor("Hierarchy")
        if hierarchy!= None:
            hierarchy.UpdateHierarchy()
        InspectorWindowEditor.Instance.ShowInspector("")
        for gameObject in self.gameObjectsList:
            gameObject.Destroy()
        self.gameObjects.clear()
        EnvironmentSystem.Instance.UpdateInstances()

    @staticmethod
    def OnDoubleClickedProject(assetItem: AssetItem):
        GlobalVars.Particle.sceneManager.LoadScene(assetItem)

AssetItem.AddCallFunction(".scene","OnDoubleClickedProject", Scene.OnDoubleClickedProject)