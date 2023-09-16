from Particle.Modules.Includes import *
from Particle.Modules.Includes import ctk
from Particle.Modules.LanguageSystem import LanguageSystem
from Particle.Modules.Directory import *
from Particle.WindowEditor.WindowEditor import WindowEditor
from Particle.Types.AssetItem import AssetItem
from Particle.Types.Object import Object


class AssetSystem:
    Scanning = False
    def __init__(self,_Particle):
        self.Particle = _Particle
        self.DisableNextRefresh = False
        self.assetsPath = os.path.join(self.Particle.config.get("projectPath"), "Assets")
        self.varInfo= tkinter.StringVar()
        self.labelInfo = None
        self.ScanAssets()
        self.Particle.window.bind("<FocusIn>", self.OnRefreshAssets)
        
    #attribut
    @property
    def assets(self):
        values = Object.Objects.values()
        return [x for x in values if isinstance(x, AssetItem)]

    def ScanAssets(self):
        if AssetSystem.Scanning:
            return
        AssetSystem.Scanning = True
        for root, dirs, files in os.walk(self.assetsPath):
            for name in files:
                path = os.path.join(root, name)
                if path.endswith(".meta"):
                    #check if the asset exist
                    if not os.path.exists(path[:-5]):
                        #check if the asset is in the list
                        loaded = False
                        for asset in self.assets:
                            if asset.metaPath == path:
                                loaded = True
                                asset.Destroy()
                                break
                        if not loaded:
                            #remove the meta file
                            os.remove(path)
                    continue
                if self.labelInfo is not None:
                    self.varInfo.set(path)
                    self.labelInfo.update()
                AssetItem.create(path)
        #vériier si les assets sont encore présent
        for asset in self.assets:
            if not os.path.exists(asset.path):
                asset.Destroy()
        AssetSystem.Scanning = False

    def OnRefreshAssets(self,event):
        if self.DisableNextRefresh:
            self.DisableNextRefresh = False
            return
        if AssetSystem.Scanning:
            return
        frame = self.Particle.SetSecondMainFrame()
        if frame == None:
            return
        #draw Big Label in the middle
        self.label = ctk.CTkLabel(frame, text=LanguageSystem.GetText("Actualisation des Assets..."),
                                  fg_color="transparent", compound="top",
                                  font=ctk.CTkFont(size=40, weight="bold"))
        self.label.pack(fill=BOTH, expand=True)

        self.labelInfo = ctk.CTkLabel(frame, textvariable=self.varInfo,
                                  fg_color="transparent", compound="top",
                                  font=ctk.CTkFont(size=20, weight="bold"))
        self.labelInfo.pack(fill=BOTH, expand=True)
        self.label.update()
        self.ScanAssets()
        self.labelInfo = None
        self.Particle.SetMainFrame()
        project = self.Particle.GetEditor("Project")
        if project is not None:
            project.Update()
        