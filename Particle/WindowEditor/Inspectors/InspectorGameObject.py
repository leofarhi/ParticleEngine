from Particle.Modules.Includes import *
from Particle.WindowEditor.WindowEditor import WindowEditor
from Particle.Modules.LanguageSystem import LanguageSystem
from Particle.Modules.Directory import *
from Particle.Modules.Screen import GetScreenSize
from Particle.WindowEditor.InspectorWindowEditor import InspectorWindowEditor

class InspectorGameObject:
    name = "GameObject"
    def __init__(self,inspectorWindowEditor) -> None:
        #print("init inspector: " + self.name)
        self.name = InspectorGameObject.name
        self.inspectorWindowEditor = inspectorWindowEditor

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
        self.Particle.assetSystem.DisableNextRefresh = True
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

    def OnLostFocus(self,event):
        self.Destroy()

InspectorWindowEditor.AddInspector(InspectorGameObject)