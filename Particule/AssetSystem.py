from Particule.Modules.Includes import *
from Particule.Modules.Includes import ctk
from Particule.Modules.LanguageSystem import LanguageSystem
from Particule.Modules.Directory import *
from Particule.WindowEditor.WindowEditor import WindowEditor
from Particule.Types.AssetItem import AssetItem


class AssetSystem:
    Scanning = False
    def __init__(self,_Particule):
        self.Particule = _Particule
        self.assets = {}
        self.assetsPath = os.path.join(self.Particule.config.get("projectPath"), "Assets")
        self.varInfo= tkinter.StringVar()
        self.labelInfo = None
        self.ScanAssets()
        self.Particule.window.bind("<FocusIn>", self.OnRefreshAssets)
        

    def ScanAssets(self):
        if AssetSystem.Scanning:
            return
        AssetSystem.Scanning = True
        self.assets = {}
        for root, dirs, files in os.walk(self.assetsPath):
            for name in files:
                path = os.path.join(root, name)
                if path.endswith(".meta"):
                    continue
                if self.labelInfo is not None:
                    self.varInfo.set(path)
                    self.labelInfo.update()
                asset = AssetItem(path)
                self.assets[asset.uuid] = asset
        AssetSystem.Scanning = False

    def OnRefreshAssets(self,event):
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
        