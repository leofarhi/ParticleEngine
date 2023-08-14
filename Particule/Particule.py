import subprocess
import platform
from Particule.Modules.Screen import GetScreenSize
from Particule.Modules.Includes import *
from Particule.Modules.LanguageSystem import LanguageSystem
from Particule.Modules.Directory import *
from Particule.WindowEditor.WindowEditor import WindowEditor
from Particule.WindowEditor.HubWindowEditor import HubWindowEditor
from Particule.WindowEditor.SceneWindowEditor import SceneWindowEditor
from Particule.ScreenOrganization import ScreenOrganization
from Particule.AssetSystem import AssetSystem
from Particule.SceneManager import SceneManager

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class Particule:
    version = "2023.1b"
    def __init__(self):
        GlobalVars.Particule = self
        self.window = None
        self.config = {
            "name": "",
            "projectPath": "",
            "template": "",
            "language":"",
            "version":""
        }

    def HubWindow(self):
        hub = HubWindowEditor()
        hub.Pack()

    def SetSecondMainFrame(self):
        if self.SecondFrame != None:
            return None
        self.MainFrame.pack_forget()
        self.SecondFrame = ctk.CTkFrame(self.window)
        self.SecondFrame.pack(fill=BOTH, expand=True)
        return self.SecondFrame

    def SetMainFrame(self):
        if self.SecondFrame != None:
            self.SecondFrame.destroy()
            self.SecondFrame = None
        self.MainFrame.pack(fill=BOTH, expand=True)

    def Start(self):
        self.window = ctk.CTk()
        self.window.title('Particule - ' + Particule.version)
        screen_size = GetScreenSize()
        self.window.geometry(str(screen_size[0]) + "x" + str(screen_size[1]))
        WindowEditor.LoadWindowIcon(self)
        #Mettre en plein écran
        self.window.attributes('-fullscreen', False)

        pathProject = self.config.get("projectPath")
        try:
            DeleteDir(os.path.join(pathProject, "Library", "tmp"))
            DeleteDir(os.path.join(pathProject, "Build"))
        except:
            pass
        CreateDir(os.path.join(pathProject, "Assets"))
        CreateDir(os.path.join(pathProject, "Library"))
        CreateDir(os.path.join(pathProject, "Library", "tmp"))
        CreateDir(os.path.join(pathProject, "Build"))

        self.MainFrame = ctk.CTkFrame(self.window)
        self.MainFrame.pack(fill=BOTH, expand=True)
        self.SecondFrame = None

        self.sceneManager = SceneManager(self)
        self.screenOrganization = ScreenOrganization(self)
        self.assetSystem = AssetSystem(self)

        #Quitter
        self.window.protocol("WM_DELETE_WINDOW", self.Quit)
        self.window.mainloop()
    
    def Restart(self):
        self.window.destroy()
        self.Start()

    def Quit(self):
        if messagebox.askokcancel(LanguageSystem.GetText("Quit"),
                                  LanguageSystem.GetText("Voulez-vous vraiment quitter ?")):
            self.window.destroy()

