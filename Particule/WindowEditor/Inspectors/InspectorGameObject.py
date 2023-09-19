from Particule.Modules.Includes import *
from Particule.WindowEditor.WindowEditor import WindowEditor
from Particule.Modules.LanguageSystem import LanguageSystem
from Particule.Modules.Directory import *
from Particule.Modules.Screen import GetScreenSize
from Particule.WindowEditor.InspectorWindowEditor import InspectorWindowEditor
from Particule.Modules.MyCustomTkinter.MyToggledFrame import MyToggledFrame
from Particule.WindowEditor.CustomComponentEditor import *

class InspectorGameObject:
    name = "GameObject"
    def __init__(self,inspectorWindowEditor) -> None:
        #print("init inspector: " + self.name)
        self.name = InspectorGameObject.name
        self.inspectorWindowEditor = inspectorWindowEditor
        self.Particule = inspectorWindowEditor.Particule

        self.frame = ctk.CTkFrame(self.inspectorWindowEditor.window)

        self.header_frame = ctk.CTkFrame(self.frame,height=50)
        self.header_frame.pack(side=TOP, fill=X)

        self.body_frame = ctk.CTkScrollableFrame(self.frame)
        self.body_frame.pack(side=TOP, fill=BOTH, expand=True)

        #add Button in footer centred without frame
        self.AddComponentButton = ctk.CTkButton(self.frame,
                                                text=LanguageSystem.GetText("Ajouter un Component"),
                                                command=partial(AddComponentWindow, self))
        #center button
        self.AddComponentButton.pack(side=BOTTOM, fill=X)

        #Header
        self.varName = tkinter.StringVar()
        self.varActive = tkinter.BooleanVar()
        self.varStatic = tkinter.BooleanVar()
        self.varTag = tkinter.StringVar()
        self.varLayer = tkinter.StringVar()

        #configure header -> grid fill x
        self.header_frame.grid_columnconfigure(0, weight=0)
        self.header_frame.grid_columnconfigure(1, weight=1)
        self.header_frame.grid_columnconfigure(2, weight=0)
        self.header_frame.grid_columnconfigure(3, weight=1)


        self.CheckbuttonActive = ctk.CTkSwitch(self.header_frame,width=24,
                                                 text="",
                                                 variable=self.varActive)
        self.CheckbuttonActive.grid(row=0, column=0, sticky="w")

        self.EntryName = ctk.CTkEntry(self.header_frame, textvariable=self.varName)
        #expand entry
        self.EntryName.grid(row=0, column=1, sticky="we", columnspan=3)

        self.CheckbuttonStatic = ctk.CTkCheckBox(self.header_frame, width=1,
                                                    text="Static",
                                                    variable=self.varStatic)
        self.CheckbuttonStatic.grid(row=0, column=4, sticky="e",padx=15)

        #make dropdown with title in second row
        self.DropdownLabel = ctk.CTkLabel(self.header_frame, text="Tag")
        self.DropdownLabel.grid(row=1, column=0, sticky="w")
        self.Dropdown = ctk.CTkComboBox(self.header_frame, variable=self.varTag)
        self.Dropdown.grid(row=1, column=1, sticky="we")

        #make dropdown with title in second row
        self.DropdownLabel = ctk.CTkLabel(self.header_frame, text="Layer", width=1)
        self.DropdownLabel.grid(row=1, column=2, sticky="e",padx=5)
        self.Dropdown = ctk.CTkComboBox(self.header_frame, variable=self.varLayer)
        self.Dropdown.grid(row=1, column=3, sticky="we", columnspan=2)

        #bind header
        self.varName.trace("w", self.OnNameChanged)
        self.varActive.trace("w", self.OnActiveChanged)
        self.varStatic.trace("w", self.OnStaticChanged)
        self.varTag.trace("w", self.OnTagChanged)
        self.varLayer.trace("w", self.OnLayerChanged)


        self.CurrentGameObjectEdited = None
    
    def OnNameChanged(self,*args):
        if self.CurrentGameObjectEdited == None:
            return
        self.CurrentGameObjectEdited.name = self.varName.get()
        hierarchy = self.Particule.GetEditor("Hierarchy")
        if hierarchy!= None:
            hierarchy.UpdateHierarchy(self.CurrentGameObjectEdited)

    def OnActiveChanged(self,*args):
        if self.CurrentGameObjectEdited == None:
            return
        self.CurrentGameObjectEdited.activeSelf = self.varActive.get()

    def OnStaticChanged(self,*args):
        if self.CurrentGameObjectEdited == None:
            return
        self.CurrentGameObjectEdited.isStatic = self.varStatic.get()

    def OnTagChanged(self,*args):
        return
        if self.CurrentGameObjectEdited == None:
            return
        self.CurrentGameObjectEdited.tag = self.varTag.get()

    def OnLayerChanged(self,*args):
        return
        if self.CurrentGameObjectEdited == None:
            return
        self.CurrentGameObjectEdited.layer = self.varLayer.get()

    def UpdateInspector(self,gameObject=[],*args,**kwargs):
        #forget all children of body_frame
        for child in self.body_frame.winfo_children():
            child.forget()
        if len(gameObject) == 0:
            return
        gameObject = gameObject[0]
        self.CurrentGameObjectEdited = gameObject
        self.varName.set(gameObject.name)
        self.varActive.set(gameObject.activeSelf)
        self.varStatic.set(gameObject.isStatic)
        #self.varTag.set(gameObject.tag)
        #self.varLayer.set(gameObject.layer)
        #update dropdown
        if gameObject.frameOfComponents == None:
            gameObject.frameOfComponents = {}
            gameObject.frameOfComponents["MainFrame"] = ctk.CTkFrame(self.body_frame)
            components = {}
            for component in gameObject.components:
                pack = {}
                pack["ToggledFrame"] = MyToggledFrame(gameObject.frameOfComponents["MainFrame"], text=component.ComponentName,border_color="white",border_width=1)
                pack["ToggledFrame"].pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
                pack["ToggledFrame"].Open()
                pack["ComponentDrawer"] = ComponentDrawer.New(component.ComponentName)(pack["ToggledFrame"].sub_frame,component)
                pack["ComponentDrawer"].SerializeFields()
                components[component.ComponentName] = pack
        gameObject.frameOfComponents["MainFrame"].pack(side=TOP, fill=X)


    def Pack(self):
        self.frame.pack(fill=BOTH, expand=True)

    def Unpack(self):
        self.frame.pack_forget()


class AddComponentWindow(WindowEditor):
    def __init__(self, master=None):
        if type(master) is not InspectorGameObject:
            raise Exception("AddComponentWindow: master type not supported")
        self.master = master
        self.ButtonAdd = self.master.AddComponentButton
        super().__init__(None,"Ajouter un Component",ToplevelClass=tkinter.Toplevel)
        if self.WindowMode != "toplevel":
            raise Exception("AddComponentWindow: WindowMode not supported")
        self.MainFrame = ctk.CTkFrame(self.window,corner_radius=0,border_width=5)
        self.MainFrame.pack(fill=BOTH, expand=True)
        geo = str(self.ButtonAdd.winfo_width()) + "x250"
        geo+= "+" + str(self.ButtonAdd.winfo_rootx()) + "+" + str(self.ButtonAdd.winfo_rooty()) #+self.ButtonAdd.winfo_height())
        self.window.geometry(geo)
        self.window.resizable(False, False)
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)

        #make frame header
        self.HeaderFrame = ctk.CTkFrame(self.MainFrame,height=50)
        self.HeaderFrame.pack(side=TOP, fill=X)

        #make frame body scrollable
        self.BodyFrame = ctk.CTkScrollableFrame(self.MainFrame)
        self.BodyFrame.pack(side=TOP, fill=BOTH, expand=True)

        #Header
        self.varSearch = tkinter.StringVar()
        #self.varSearch.trace("w", self.OnSearch)
        self.EntrySearch = ctk.CTkEntry(self.HeaderFrame, textvariable=self.varSearch)
        self.EntrySearch.pack(side=LEFT, fill=X, expand=True)

        self.window.focus_force()
        self.window.focus_set()
        self.window.bind("<FocusOut>", self.OnLostFocus)
        self.Pack()
        self.Particule.assetSystem.DisableNextRefresh = True

    def OnLostFocus(self,event):
        self.Particule.assetSystem.DisableNextRefresh = True
        self.Destroy()

InspectorWindowEditor.AddInspector(InspectorGameObject)