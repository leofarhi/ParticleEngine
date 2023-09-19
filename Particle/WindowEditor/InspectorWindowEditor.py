from Particle.Modules.Includes import *
from Particle.WindowEditor.WindowEditor import WindowEditor
from Particle.Modules.LanguageSystem import LanguageSystem
from Particle.Modules.Directory import *
from Particle.Modules.Screen import GetScreenSize


class InspectorWindowEditor(WindowEditor):
    __inspectors__ = []
    Instance = None
    def __init__(self, master=None):
        super().__init__(master,"Inspector")
        InspectorWindowEditor.Instance = self
        self.name = "Inspector"
        self.inspectorsRuntimes = []
        for i in InspectorWindowEditor.__inspectors__:
            self.inspectorsRuntimes.append(i(self))

        self.currentInspector = None

    @AddCallBackToStack("SelectedGameObjectsChanged")
    def UpdateInspector(*args,**kwargs):
        self = InspectorWindowEditor.Instance
        if self.currentInspector != None:
            self.currentInspector.UpdateInspector(*args,**kwargs)

    def AddInspector(inspector):
        InspectorWindowEditor.__inspectors__.append(inspector)
        if InspectorWindowEditor.Instance is not None:
            InspectorWindowEditor.Instance.inspectorsRuntimes(inspector(InspectorWindowEditor.Instance))

    def ShowInspector(self,inspectorName):
        if self.currentInspector != None and self.currentInspector.name == inspectorName:
            return
        self.currentInspector = None
        for i in self.inspectorsRuntimes:
            i.Unpack()
        for i in self.inspectorsRuntimes:
            if i.name == inspectorName:
                i.Pack()
                self.currentInspector = i
                break

#load all inspectors withou import them
for i in os.listdir(os.path.dirname(__file__) + "/Inspectors"):
    if i.endswith(".py"):
        #check if not already loaded with InspectorWindowEditor.inspectors
        if not any(x.name == i[:-3] for x in InspectorWindowEditor.__inspectors__):
            #print("load inspector: " + i[:-3])
            importlib.import_module("Particle.WindowEditor.Inspectors." + i[:-3])