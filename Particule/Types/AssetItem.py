from Particule.Modules.Includes import *


class AssetItem:
    def __init__(self,path) -> None:
        self.path = path
        self.name = os.path.basename(path)
        self.extention = os.path.splitext(path)[1]
        self.type = "file" if os.path.isfile(path) else "dir"
        
        self.uuid = None
        self.config = {}
        #check if meta file exist
        self.metaPath = path + ".meta"
        if os.path.isfile(self.metaPath):
            with open(self.metaPath, "r") as f:
                self.config = json.load(f)
                self.uuid = self.config.get("uuid")
        else:
            self.uuid = str(uuid.uuid4())
            self.config = {
                "uuid":self.uuid
            }
            with open(self.metaPath, "w") as f:
                json.dump(self.config, f, indent=4)
