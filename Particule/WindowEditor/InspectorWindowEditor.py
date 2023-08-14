from Particule.Modules.Includes import *
from Particule.WindowEditor.WindowEditor import WindowEditor
from Particule.Modules.LanguageSystem import LanguageSystem
from Particule.Modules.Directory import *
from Particule.Modules.Screen import GetScreenSize


class InspectorWindowEditor(WindowEditor):
    inspectors = []
    Instance = None
    def __init__(self, master=None):
        super().__init__(master,"Inspector")
        InspectorWindowEditor.Instance = self
        self.inspectorsRuntimes = []
        for i in InspectorWindowEditor.inspectors:
            self.inspectorsRuntimes.append(i(self))

        #DEBUG
        if len(self.inspectorsRuntimes) > 0:
            self.inspectorsRuntimes[0].Pack()

    def AddInspector(inspector):
        InspectorWindowEditor.inspectors.append(inspector)
        if InspectorWindowEditor.Instance is not None:
            InspectorWindowEditor.Instance.inspectorsRuntimes(inspector(InspectorWindowEditor.Instance))

    def ShowInspector(self,inspectorName):
        for i in self.inspectorsRuntimes:
            i.Unpack()
        for i in self.inspectors:
            if i.name == self.inspectorsRuntimes:
                i.Pack()
                break

#load all inspectors withou import them
for i in os.listdir(os.path.dirname(__file__) + "/Inspectors"):
    if i.endswith(".py"):
        #check if not already loaded with InspectorWindowEditor.inspectors
        if not any(x.name == i[:-3] for x in InspectorWindowEditor.inspectors):
            #print("load inspector: " + i[:-3])
            importlib.import_module("Particule.WindowEditor.Inspectors." + i[:-3])