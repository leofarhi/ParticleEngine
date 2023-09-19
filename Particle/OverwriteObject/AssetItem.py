from Particle.Modules.Includes import *
from Particle.OverwriteObject.Object import Object
from Particle.EnvironmentSystem import *

@OverwriteObject()
class AssetItem(Object):
    @staticmethod
    def create(path):
        if os.path.isfile(path):
            #load meta
            metaPath = path + ".meta"
            if os.path.isfile(metaPath):
                with open(metaPath, "r") as f:
                    config = json.load(f)
                asset = Object.GetObject(config.get("UUID"))
                if asset:
                    if asset.FileAreEdited():
                        asset.CallBackFileEdited()
                    return asset
                else:
                    return AssetItem(path)
            else:
                #check if file is not already in the database
                for asset in GlobalVars.Particle.assetSystem.assets:
                    if asset.path == path:
                        asset.SaveMeta()
                        return asset
                return AssetItem(path)
        return None
    CallFileType = {}
    #exemple
    #CallFileType[".png"] = {
    #    "OnClickedProject": ChangeInspectorTexture,
    #    "OnDoubleClickedProject": OpenTextureInEditor,
    # }
    #CallFileType[".scene"] = {
    #    "OnDoubleClickedProject": LoadScene,
    # }

    @staticmethod
    def AddCallFunction(extension, function, callback):
        if extension not in AssetItem.CallFileType:
            AssetItem.CallFileType[extension] = {}
        AssetItem.CallFileType[extension][function] = callback

    @staticmethod
    def CallFunction(assetItem, function):
        if assetItem.extension in AssetItem.CallFileType:
            if function in AssetItem.CallFileType[assetItem.extension]:
                AssetItem.CallFileType[assetItem.extension][function](assetItem)

    def __init__(self,path,UUID = None,*args, **kwargs) -> None:
        self.UUID = None
        #absolute path
        self.path = os.path.abspath(os.path.realpath(path))
        self.name = os.path.basename(path)
        self.extension = os.path.splitext(path)[1]
        self.type = "file" if os.path.isfile(path) else "dir"

        self.config = {}
        #check if meta file exist
        self.metaPath = path + ".meta"
        IsNew = False
        if os.path.isfile(self.metaPath):
            with open(self.metaPath, "r") as f:
                self.config = json.load(f)
                if self.config.get("path") != self.path:
                    self.config["path"] = self.path
                    self.config["name"] = self.name
                    self.config["metaPath"] = self.metaPath
                if self.config.get("extension") == self.extension and self.config.get("type") == self.type:
                    super().__init__(self.config.get("UUID"),*args, **kwargs)
                else:
                    IsNew = True
        else:
            IsNew = True
        if IsNew:
            super().__init__(None,*args, **kwargs)
            self.config = super().getDict()
            SecondConfig = {
                "path": self.path,
                "metaPath": self.metaPath,
                "name": self.name,
                "extension": self.extension,
                "type": self.type,
                "lastEdit": os.path.getmtime(path),
            }
            self.config.update(SecondConfig)
            with open(self.metaPath, "w") as f:
                json.dump(self.config, f, indent=4)

    def FileAreEdited(self):
        if os.path.isfile(self.path):
            return os.path.getmtime(self.path) != self.config.get("lastEdit")
        return False
    
    def SaveMeta(self):
        if self.FileAreEdited():
            self.config["lastEdit"] = os.path.getmtime(self.path)
        with open(self.metaPath, "w") as f:
            json.dump(self.config, f, indent=4)

    def CallBackFileEdited(self):
        self.SaveMeta()
        #TODO: Call callback

    def getDict(self):
        return self.config
    
    def Destroy(self):
        if os.path.exists(self.path):
            if os.path.isfile(self.path):
                os.remove(self.path)
        if os.path.exists(self.metaPath):
            os.remove(self.metaPath)
        super().Destroy()

    def CallBackDestroy(self):
        super().CallBackDestroy()
        #TODO: Call callback

    @staticmethod
    def GetAssetItem(path):
        path = os.path.abspath(os.path.realpath(path))
        return AssetItem.create(path)
    
    @staticmethod
    def GetAssetItemFromUUID(UUID):
        obj =  Object.GetObject(UUID)
        if obj and isinstance(obj, AssetItem):
            return obj
        return None
