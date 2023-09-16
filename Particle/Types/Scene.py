from Particle.Modules.Includes import *
from Particle.Types.Object import Object
from Particle.Types.GameObject import GameObject
from Particle.Types.AssetItem import AssetItem

class Scene(Object):
    def __init__(self, UUID=None, assetItem=None):
        super().__init__(UUID)
        self.gameObjects = {}
        self.assetItem = assetItem

    @property
    def gameObjectsList(self) -> list:
        return list(self.gameObjects.values())
    
    @property
    def name(self) -> str:
        if self.assetItem is None:
            return "New Scene"
        return self.assetItem.name

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
        data = {
            "gameObjects": self.gameObjectsList,
        }
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def Load(self):
        if self.assetItem is None:
            raise Exception("No path provided")
        with open(self.assetItem.path, "r", encoding="utf-8") as file:
            data = json.load(file)
        for gameObjectDict in data["gameObjects"]:
            pass

    def Unload(self):
        pass

    @staticmethod
    def OnDoubleClickedProject(assetItem: AssetItem):
        GlobalVars.Particle.sceneManager.LoadScene(assetItem)

AssetItem.AddCallFunction(".scene","OnDoubleClickedProject", Scene.OnDoubleClickedProject)