from Particule.Modules.Includes import *
from Particule.Modules.Includes import ctk
from Particule.Modules.LanguageSystem import LanguageSystem
from Particule.Modules.Directory import *
from Particule.WindowEditor.WindowEditor import WindowEditor
from Particule.OverwriteObject.AssetItem import AssetItem
from Particule.OverwriteObject.Object import Object


class AssetSystem:
    Scanning = False
    def __init__(self,_Particule):
        self.Particule = _Particule
        self.DisableNextRefresh = False
        self.assetsPath = os.path.join(self.Particule.config.get("projectPath"), "Assets")
        self.varInfo= tkinter.StringVar()
        self.labelInfo = None
        self.Particule.window.bind("<FocusIn>", self.OnFocusIn)
        self.Particule.window.bind("<FocusOut>", self.OnFocusOut)
        self.LostFocus = datetime.datetime.now()
        
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

    def OnFocusOut(self,event):
        self.LostFocus = datetime.datetime.now()

    def OnFocusIn(self,event):
        if (datetime.datetime.now() - self.LostFocus).total_seconds() < 0.5:
            return
        self.LostFocus = datetime.datetime.now()
        self.OnRefreshAssets(event)

    def OnRefreshAssets(self,event):
        if self.DisableNextRefresh:
            self.DisableNextRefresh = False
            return
        if AssetSystem.Scanning:
            return
        frame = self.Particule.SetSecondMainFrame()
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
        self.Particule.SetMainFrame()
        project = self.Particule.GetEditor("Project")
        if project is not None:
            project.Update()
        