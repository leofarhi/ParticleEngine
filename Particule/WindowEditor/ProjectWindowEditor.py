from Particule.Modules.Includes import *
from Particule.WindowEditor.WindowEditor import WindowEditor
from Particule.Modules.LanguageSystem import LanguageSystem
from Particule.Modules.Directory import *
from Particule.Modules.Screen import GetScreenSize
from Particule.Modules.SpecialImage import SpecialImage
import os, sys
from Particule.OverwriteObject.AssetItem import AssetItem

class FolderItem:
    Size = 70
    def __init__(self,path) -> None:
        self.opened = False
        self.path = path

        self.name = os.path.basename(path)
        self.extension = os.path.splitext(path)[1]
        self.type = "file" if os.path.isfile(path) else "dir"

        self.assetItem = AssetItem.GetAssetItem(path)
        self.children = []
        self.parent = None
        if self.type == "dir":
            self.image = ProjectWindowEditor.Images["folder"]
        else:
            self.image = ProjectWindowEditor.Images[self.extension] if self.extension in ProjectWindowEditor.Images else ProjectWindowEditor.Images["file"]
        if self.image == ProjectWindowEditor.Images[".png"]:
            self.image = SpecialImage(self.path)
        self.frameImage = None
        self.frame = None

    def DrawItem(self,frame,count,columns):
        self.frameImage = ctk.CTkImage(self.image.image, size=(FolderItem.Size, FolderItem.Size))
        self.frame = ctk.CTkFrame(frame,width=FolderItem.Size,height=FolderItem.Size)
        self.frame.grid(row=count//columns,column=count%columns,padx=5,pady=5)
        name = self.name
        if len(name) > 13:
            name = name[:10] + "..."
        self.frameLabel = ctk.CTkButton(self.frame, text=name, image=self.frameImage,fg_color="transparent",
                                        compound="top", width=FolderItem.Size, height=FolderItem.Size)
        self.frameLabel.pack(fill=BOTH, expand=True)
        if len(self.name) > 13:
            CreateToolTip(self.frameLabel, text=self.name)
        self.ConfigureBindings()
        count += 1
        return count
    
    def ConfigureBindings(self):
        self.frameLabel.bind("<Button-1>", self.OnClicked)
        self.frameLabel.bind("<Double-Button-1>", self.OnDoubleClicked)
        self.frameLabel.bind("<Button-3>", self.OnRightClicked)

    def OnClicked(self,event):
        FolderItem.UnselectAll()
        self.frame.configure(fg_color="gray75")
        if self.type == "file":
            AssetItem.CallFunction(self.assetItem,"OnClickedProject")

    def UnselectAll():
        projectWindowEditor = GlobalVars.Particule.screenOrganization.windowEditors.get("Project")
        if projectWindowEditor is None:
            return
        for i in projectWindowEditor.Items:
            if i.frame:
                i.frame.configure(fg_color="transparent")

    def OnDoubleClicked(self,event):
        projectWindowEditor = GlobalVars.Particule.screenOrganization.windowEditors.get("Project")
        if projectWindowEditor is None:
            return
        if self.type == "dir":
            projectWindowEditor.currentFolder = self.path
            projectWindowEditor.UpdateFolderView()
        elif self.type == "file":
            AssetItem.CallFunction(self.assetItem,"OnDoubleClickedProject")

    def OnRightClicked(self,event):
        pass


    def Draw(listOfItems,frame,projectWindowEditor):
        width = projectWindowEditor.panedWindow.MainFrames[projectWindowEditor.FolderView].winfo_width()
        columns = (width // (FolderItem.Size+(15*2)))-1
        if columns <= 0:
            columns = 1
        count = 0
        rm = [GlobalVars.Particule.config.get("projectPath"),os.path.join(GlobalVars.Particule.config.get("projectPath"),"Assets")]
        for i in range(len(rm)):
            rm[i] = os.path.normpath(rm[i])
        if not os.path.normpath(projectWindowEditor.currentFolder) in rm:
            can = True
            if len(listOfItems) > 0:
                if listOfItems[0].name == "..":
                    can = False
            if can:
                parent = FolderItem(os.path.dirname(projectWindowEditor.currentFolder))
                parent.name = ".."
                parent.image = ProjectWindowEditor.Images["folder_back"]
                #parent.DrawItem(frame,count,columns)
                listOfItems.insert(0,parent)
                count += 1
        for i in listOfItems:
            count = i.DrawItem(frame,count,columns)


class ProjectWindowEditor(WindowEditor):
    Images = {}
    def __init__(self, master=None):
        super().__init__(master,"Project")
        self.LoadImages()

        self.panedWindow = MyPanedWindow(self.window, orient=HORIZONTAL)
        self.panedWindow.pack(fill=BOTH, expand=True)

        self.projectTreeFrame = self.panedWindow.SplitFrame()
        self.projectTreeScrollbar = ctk.CTkScrollbar(self.projectTreeFrame,orientation="vertical")
        self.projectTree = MyTreeview(self.projectTreeFrame, columns=("Path", "Type"), 
                                      selectmode="browse", show="tree",
                                        displaycolumns=(),
                                        yscrollcommand=self.projectTreeScrollbar.set)
        self.projectTreeScrollbar.configure(command=self.projectTree.yview)
        self.projectTree.heading("#0", text="Name", anchor=W)
        self.projectTree.heading("Path", text="Path", anchor=W)

        self.folder_image = SpecialImage("lib/UI/Icons/Project/folder_small.png").imageTk
        self.file_image = SpecialImage("lib/UI/Icons/Project/textfile_small.png").imageTk
        
        self.projectTree.pack(side=LEFT, fill=BOTH, expand=True)
        self.projectTreeScrollbar.pack(side=LEFT, fill=Y)
        
        self.FolderView = self.panedWindow.SplitFrame()
        self.FolderViewScroll = ctk.CTkScrollableFrame(self.FolderView)
        self.FolderViewScroll.pack(side=LEFT, fill=BOTH, expand=True)


        #ProjectTree
        self.UpdateTree()

        #FolderView
        self.currentFolder = os.path.join(self.Particule.config.get("projectPath"), "Assets")
        self.Items = []
        self.UpdateFolderView()

        self.projectTree.bind("<Double-Button-1>", self.OnDoubleClickTree)


        self.UpdateAppearanceMode()

        self.FolderView.bind("<Configure>", self.RedrawFolderView)

        #ctk.set_appearance_mode("Light")

    def OnDoubleClickTree(self,event):
        item = self.projectTree.identify('item',event.x,event.y)
        if item == "":
            return
        if self.projectTree.item(item,"values")[1] == "dir":
            path = self.projectTree.item(item,"values")[0]
            self.currentFolder = path
            self.UpdateFolderView()

    def UpdateTree(self):
        #save open folders
        openedFolders = []
        #recursively get open folders
        def GetOpenFolders(item):
            if self.projectTree.item(item,"open") == True:
                openedFolders.append(item)
            for i in self.projectTree.get_children(item):
                GetOpenFolders(i)
        GetOpenFolders("")
        #clear All tree items
        for i in self.projectTree.get_children():
            self.projectTree.delete(i)
        
        files = []# (path, type)
        folders = []# (path, type)
        stack = [self.Particule.config.get("projectPath")]
        while len(stack) > 0:
            path = stack.pop()
            for i in os.listdir(path):
                if i.startswith(".") or os.path.splitext(i)[1] == ".meta":
                    continue
                if os.path.isdir(path + "/" + i):
                    folders.append((path + "/" + i, "dir"))
                    stack.append(path + "/" + i)
                else:
                    files.append((path + "/" + i, "file"))
        #root
        self.projectTree.insert("", 0, self.Particule.config.get("projectPath"), text=os.path.basename(self.Particule.config.get("projectPath")), values=(self.Particule.config.get("projectPath"), "dir"), tags=("dir"), image=self.folder_image)
        #folders
        for i in folders:
            self.projectTree.insert(os.path.dirname(i[0]), "end", i[0], text=os.path.basename(i[0]), values=i, tags=("dir"), image=self.folder_image)
        #files
        for i in files:
            self.projectTree.insert(os.path.dirname(i[0]), "end", i[0], text=os.path.basename(i[0]), values=i, tags=("file"), image=self.file_image)
        #open folders
        for i in openedFolders:
            #get item from path and open it
            #check if item exists
            if self.projectTree.exists(i):
                self.projectTree.item(i,open=True)
    def UpdateFolderView(self):
        for i in self.Items:
            if i.frame:
                i.frame.destroy()
        files = os.listdir(self.currentFolder)
        self.Items = []
        for i in files:
            #si son extension est .meta on ne l'ajoute pas
            if os.path.splitext(i)[1] == ".meta":
                continue
            self.Items.append(FolderItem(self.currentFolder + "/" + i))
        self.Items.sort(key=lambda x: x.type+x.name)
        self.RedrawFolderView()

    def RedrawFolderView(self,event=None):
        #clear widgets in FolderView (grid)
        for i in self.Items:
            if i.frame:
                i.frame.destroy()
        FolderItem.Draw(self.Items,self.FolderViewScroll,self)

    def Update(self):
        self.UpdateFolderView()
        self.UpdateTree()

    def LoadImages(self):
        ProjectWindowEditor.Images["folder"] = SpecialImage("lib/UI/Icons/Project/folder_big.png")
        ProjectWindowEditor.Images["file"] = SpecialImage("lib/UI/Icons/Project/textfile_big.png")
        ProjectWindowEditor.Images["folder_back"] = SpecialImage("lib/UI/Icons/Project/up_big.png")
        path = "lib/UI/Icons/Project/Extensions/"
        for i in os.listdir(path):
            imgPath = path + i
            name = os.path.splitext(i)[0]
            img = SpecialImage(imgPath)
            extension = name.split(".")
            del extension[0]
            for j in extension:
                ProjectWindowEditor.Images["."+j] = img