from Particle.Modules.Includes import *
from Particle.Modules.LanguageSystem import LanguageSystem
from Particle.Modules.Directory import *
from Particle.WindowEditor.WindowEditor import WindowEditor
from Particle.WindowEditor.SceneWindowEditor import SceneWindowEditor
from Particle.WindowEditor.HierarchyWindowEditor import HierarchyWindowEditor
from Particle.WindowEditor.InspectorWindowEditor import InspectorWindowEditor
from Particle.WindowEditor.ProjectWindowEditor import ProjectWindowEditor
from Particle.WindowEditor.ConsoleWindowEditor import ConsoleWindowEditor
from Particle.WindowEditor.BuildSettingsWindowEditor import BuildSettingsWindowEditor
from Particle.WindowEditor.PreferencesWindowEditor import PreferencesWindowEditor
from Particle.WindowEditor.ProjectSettingsWindowEditor import ProjectSettingsWindowEditor
from Particle.Modules.MyCustomTkinter.MyMenu import MyMenu

class SplitFrame(MyPanedWindow):
    def __init__(self, master, orient, **kwargs):
        super().__init__(master, orient=orient, **kwargs)
        self.orient = orient
        self.master = master

    def Split(self,*args,**kwargs):
        frame = self.SplitFrame(*args,**kwargs)
        tabview = MyTabview(frame,bg_color="transparent")
        #change sticky grid to "ns"
        tabview.pack(side=LEFT, fill=BOTH, expand=True)
        self.MainFrames[tabview] = frame
        return tabview
    

class ScreenOrganization:
    def __init__(self,_Particle):
        self.Particle = _Particle
        
        fn = self.Particle.MainFrame
        #make Header bar
        Header = ctk.CTkFrame(fn, height=50)
        Header.pack(side=TOP, fill=X)
        #make Body
        Body = ctk.CTkFrame(fn)
        Body.pack(side=TOP, fill=BOTH, expand=True)

        self.MainMenu = MyMenu(self.Particle.window)
        self.Particle.window.config(menu=self.MainMenu)
        
        SplitCenter = SplitFrame(Body, orient=VERTICAL)
        SplitCenter.pack(side=TOP, fill=BOTH, expand=True)

        Top = SplitCenter.SplitFrame(height=600)
        SplitCenter.MainFrames[Top].configure(height=600)
        BottomTabs = SplitCenter.Split()

        SplitTop = SplitFrame(Top, orient=HORIZONTAL)
        SplitTop.pack(side=TOP, fill=BOTH, expand=True)
        TopLeftTabs = SplitTop.Split(width=300)
        TopCenterTabs = SplitTop.Split(width=1100)
        SplitTop.MainFrames[TopCenterTabs].configure(width=1100)
        TopRightTabs = SplitTop.Split(width=500)

        self.windowEditors = {}

        scene = SceneWindowEditor(TopCenterTabs)
        scene.Pack()
        self.windowEditors["Scene"] = scene

        hierarchy = HierarchyWindowEditor(TopLeftTabs)
        hierarchy.Pack()
        self.windowEditors["Hierarchy"] = hierarchy

        inspector = InspectorWindowEditor(TopRightTabs)
        inspector.Pack()
        self.windowEditors["Inspector"] = inspector

        project = ProjectWindowEditor(BottomTabs)
        project.Pack()
        self.windowEditors["Project"] = project
        
        console = ConsoleWindowEditor(BottomTabs)
        console.Pack()
        self.windowEditors["Console"] = console

    def SaveInterfaceOrganization(self):
        #get children of Body
        root = None
        for i in self.Particle.MainFrame.winfo_children():
            if type(i) is SplitFrame:
                root = i
                break
        if root is None:
            return
        def RecursiveSave(node):
            for child in node.winfo_children():
                if type(child) is SplitFrame:
                    RecursiveSave(child)
                pass
        #à terminer
    def LoadInterfaceOrganization(self):
        pass


