from Particle.Modules.Includes import *
from Particle.WindowEditor.WindowEditor import WindowEditor
from Particle.Modules.LanguageSystem import LanguageSystem
from Particle.Modules.Directory import *
from Particle.Modules.Screen import GetScreenSize
from Particle.Modules.LanguageSystem import LanguageSystem

class HubWindowEditor(WindowEditor):
    def __init__(self):
        super().__init__(None,'Particle - Hub')
        screen_size = GetScreenSize()
        self.SetSize(screen_size[0]//2, screen_size[1]//2)
        if self.WindowMode == "window":
            self.window.resizable(False, False)
            self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.LoadHubConfig()

        
        #faire une frame qui prend tout la fenetre avec pack
        self.main_frame = ctk.CTkFrame(self.window, corner_radius=0)
        self.main_frame.pack(fill=tkinter.BOTH, expand=tkinter.YES)

        # configure grid layout (4x4)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure((2, 3), weight=0)
        self.main_frame.grid_rowconfigure((0, 1, 2), weight=1)

        #faire un systeme de tab pour les projets, installations, apprendre, parametres
        #quand on clique sur un bouton, on change la frame du milieu

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self.main_frame, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.ImageProject = ctk.CTkImage(light_image=Image.open("lib/UI/Icons/Hub/project_light.png"),
                                         dark_image=Image.open("lib/UI/Icons/Hub/project_dark.png"),
                                         size=(20, 20))
        self.ImageInstall = ctk.CTkImage(light_image=Image.open("lib/UI/Icons/Hub/install_light.png"),
                                            dark_image=Image.open("lib/UI/Icons/Hub/install_dark.png"),
                                          size=(20, 20))
        self.ImageLearn = ctk.CTkImage(light_image=Image.open("lib/UI/Icons/Hub/learn_light.png"),
                                            dark_image=Image.open("lib/UI/Icons/Hub/learn_dark.png"),
                                        size=(20, 20))
        self.ImageSettings = ctk.CTkImage(light_image=Image.open("lib/UI/Icons/Hub/settings_light.png"),
                                            dark_image=Image.open("lib/UI/Icons/Hub/settings_dark.png"),
                                           size=(20, 20))

        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text=LanguageSystem.GetText("Projets"),
                                              corner_radius=0, height=40, border_spacing=10,
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.ImageProject, anchor="w",
                                                command=partial(self.ChangeTab, 1))
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, text=LanguageSystem.GetText("Installations"),
                                              corner_radius=0, height=40, border_spacing=10,
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.ImageInstall, anchor="w",
                                                command=partial(self.ChangeTab, 2))
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = ctk.CTkButton(self.sidebar_frame, text=LanguageSystem.GetText("Apprendre"),
                                              corner_radius=0, height=40, border_spacing=10,
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.ImageLearn, anchor="w",
                                                command=partial(self.ChangeTab, 3))
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = ctk.CTkButton(self.sidebar_frame, text=LanguageSystem.GetText("Paramètres"),
                                              corner_radius=0, height=40, border_spacing=10,
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.ImageSettings, anchor="w",
                                                command=partial(self.ChangeTab, 4))
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)

        # create content frame with widgets
        #Tab 1 : Projets
        self.content_frame_Projets = ctk.CTkFrame(self.main_frame)
        # create header frame with widgets qui rempli le haut Horizontalement avec pack
        self.content_frame_Projets_header = ctk.CTkFrame(self.content_frame_Projets)
        self.content_frame_Projets_header.pack(fill=tkinter.X)
        #faire un label pour le titre à gauche : Projets
        self.content_frame_Projets_header_label = ctk.CTkLabel(self.content_frame_Projets_header, text=LanguageSystem.GetText("Projets"),
                                                                font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"))
        self.content_frame_Projets_header_label.pack(side=tkinter.LEFT, padx=20, pady=10)
        #faire un bouton pour creer un nouveau projet
        self.content_frame_Projets_header_button_new = ctk.CTkButton(self.content_frame_Projets_header, text=LanguageSystem.GetText("Nouveau projet"),
                                                                    command=self.MainButtonCreateNewProject)
        self.content_frame_Projets_header_button_new.pack(side=tkinter.RIGHT, padx=20, pady=10)
        #faire un bouton pour ouvrir un projet
        self.content_frame_Projets_header_button_open = ctk.CTkButton(self.content_frame_Projets_header, text=LanguageSystem.GetText("Ouvrir un projet"),
                                                                      fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"], hover_color=("gray70", "gray30"), border_width=1,
                                                                    command=self.OnAddProject)
        self.content_frame_Projets_header_button_open.pack(side=tkinter.RIGHT, padx=20, pady=10)
        #faire un une barre de recherche pour les projets
        self.content_frame_Projets_header_search = ctk.CTkEntry(self.content_frame_Projets_header, placeholder_text=LanguageSystem.GetText("Rechercher"))
        self.content_frame_Projets_header_search.pack(fill=tkinter.X, padx=20, pady=10)
        # create body frame with widgets qui rempli le bas avec pack
        self.content_frame_Projets_body = ctk.CTkFrame(self.content_frame_Projets)
        self.content_frame_Projets_body.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        #faire une liste de projet
        self.scrollable_frameProjet = ctk.CTkScrollableFrame(self.content_frame_Projets_body)
        self.scrollable_frameProjet.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        
        #load list of projects
        self.ShowListProjects()

        self.ChangeTab(1)

        #faire une frame qui prend tout la fenetre avec pack
        self.NewProject_frame = ctk.CTkFrame(self.window, corner_radius=0)
        #self.NewProject_frame.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        #faire un Header avec le titre : Nouveau projet
        self.NewProject_frame_header = ctk.CTkFrame(self.NewProject_frame)
        self.NewProject_frame_header.pack(fill=tkinter.X)
        #faire un label pour le titre au centre : Nouveau projet
        self.NewProject_frame_header_label = ctk.CTkLabel(self.NewProject_frame_header, text=LanguageSystem.GetText("Nouveau projet"),
                                                                font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"))
        self.NewProject_frame_header_label.pack(side=tkinter.LEFT, padx=20, pady=10)
        #faire la frame du body
        self.NewProject_frame_body = ctk.CTkFrame(self.NewProject_frame)
        self.NewProject_frame_body.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        #faire une sidebar à droite avec les options
        self.NewProject_frame_body_sidebar = ctk.CTkFrame(self.NewProject_frame_body, width=140, corner_radius=0)
        self.NewProject_frame_body_sidebar.pack(fill=tkinter.Y, side=tkinter.RIGHT)
        #faire un label pour le titre à gauche : Paramètres du projet
        self.NewProject_frame_body_sidebar_label = ctk.CTkLabel(self.NewProject_frame_body_sidebar, text=LanguageSystem.GetText("Paramètres du projet"),
                                                                font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"))
        self.NewProject_frame_body_sidebar_label.pack(side=tkinter.TOP, padx=20, pady=10)

        #Label pour le nom du projet
        self.NewProject_frame_body_sidebar_label_name = ctk.CTkLabel(self.NewProject_frame_body_sidebar, text=LanguageSystem.GetText("Nom du projet"),
                                                                font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"))
        self.NewProject_frame_body_sidebar_label_name.pack(side=tkinter.TOP, anchor="w", padx=20)
        #faire un entry pour le nom du projet
        self.var_name = tkinter.StringVar()
        self.NewProject_frame_body_sidebar_entry_name = ctk.CTkEntry(self.NewProject_frame_body_sidebar, placeholder_text=LanguageSystem.GetText("Nom du projet"),
                                                                        textvariable=self.var_name)
        self.NewProject_frame_body_sidebar_entry_name.pack(fill=tkinter.X, padx=20, pady=10)
        #Label pour le path du projet
        self.NewProject_frame_body_sidebar_label_path = ctk.CTkLabel(self.NewProject_frame_body_sidebar, text=LanguageSystem.GetText("Path du projet"),
                                                                font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"))
        self.NewProject_frame_body_sidebar_label_path.pack(side=tkinter.TOP, anchor="w", padx=20)
        #faire une frame pour le path
        self.NewProject_frame_body_sidebar_frame_path = ctk.CTkFrame(self.NewProject_frame_body_sidebar)
        self.NewProject_frame_body_sidebar_frame_path.pack(fill=tkinter.X, padx=20, pady=10)
        #faire un entry pour le path du projet
        self.var_path = tkinter.StringVar()
        self.NewProject_frame_body_sidebar_entry_path = ctk.CTkEntry(self.NewProject_frame_body_sidebar_frame_path, placeholder_text=LanguageSystem.GetText("Path du projet"),
                                                                     textvariable=self.var_path)
        self.NewProject_frame_body_sidebar_entry_path.pack(side=tkinter.LEFT)
        #faire un bouton pour choisir le path du projet
        self.NewProject_frame_body_sidebar_button_path = ctk.CTkButton(self.NewProject_frame_body_sidebar_frame_path,width=10, text=LanguageSystem.GetText("Parcourir")
                                                                          ,command=self.OnSelectEmplacementNewProject)
        self.NewProject_frame_body_sidebar_button_path.pack(side=tkinter.RIGHT)
        #faire une barre de separation dans la sidebar
        self.NewProject_frame_body_sidebar_separator = ttk.Separator(self.NewProject_frame_body_sidebar, orient="horizontal")
        self.NewProject_frame_body_sidebar_separator.pack(fill=tkinter.X, padx=20, pady=10)
        #faire un label dans la sidebar pour la description des templates
        self.NewProject_frame_body_sidebar_label_template = ctk.CTkLabel(self.NewProject_frame_body_sidebar, text=LanguageSystem.GetText("Templates"),
                                                                font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"))
        self.NewProject_frame_body_sidebar_label_template.pack(side=tkinter.TOP, padx=20, pady=10)
        #faire le body à gauche
        self.NewProject_frame_body_body = ctk.CTkFrame(self.NewProject_frame_body)
        self.NewProject_frame_body_body.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        #faire une scrollbarframe pour les templates
        self.NewProject_frame_body_body_scrollbarframe = ctk.CTkScrollableFrame(self.NewProject_frame_body_body)
        self.NewProject_frame_body_body_scrollbarframe.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        #faire une frame pour les templates

        #faire une barre tout en bas avec un bouton pour creer le projet
        self.NewProject_frame_footer = ctk.CTkFrame(self.NewProject_frame)
        self.NewProject_frame_footer.pack(fill=tkinter.X, side=tkinter.BOTTOM)
        #faire un bouton pour creer le projet
        self.NewProject_frame_footer_button_create = ctk.CTkButton(self.NewProject_frame_footer, text=LanguageSystem.GetText("Créer"),
                                                                   command=self.OnCreateNewProject)
        self.NewProject_frame_footer_button_create.pack(side=tkinter.RIGHT, padx=20, pady=10)
        #faire un bouton pour annuler
        self.NewProject_frame_footer_button_cancel = ctk.CTkButton(self.NewProject_frame_footer, text=LanguageSystem.GetText("Annuler"),
                                                                      fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"], hover_color=("gray70", "gray30"), border_width=1,
                                                                    command=self.cancelNewProject)
        self.NewProject_frame_footer_button_cancel.pack(side=tkinter.RIGHT, padx=20, pady=10)

    def LoadHubConfig(self):
        self.config = {
            "projects": [],
        }
        #check if file exists in lib/projects.json
        if not os.path.exists("lib/hub.json"):
            #if not, create it
            with open("lib/hub.json", "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        with open("lib/hub.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)
        #check si le path des projets existe
        projects = self.config["projects"]
        count = 0
        while count < len(projects):
            try:
                if not os.path.exists(projects[count]["projectPath"]):
                    projects.remove(projects[count])
                    continue
                else:
                    #recharger le config.proj
                    with open(os.path.join(projects[count]["projectPath"], "config.proj"), "r", encoding="utf-8") as f:
                        projects[count] = json.load(f)
            except:
                projects.remove(projects[count])
                continue
            count += 1

    def SaveHubConfig(self):
        with open("lib/hub.json", "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)

    def ShowError(self, title, message):
        messagebox.showerror(title, message)

    def MainButtonCreateNewProject(self):
        #oublier une fenetre principale (pack_forget) et repack la nouvelle fenetre
        self.var_name.set("")
        self.var_path.set("")
        self.main_frame.pack_forget()
        self.NewProject_frame.pack(fill=tkinter.BOTH, expand=tkinter.YES)

    def IsValidName(self, name):
        #le nom du projet est valide s'il est alphanumerique
        return name.isalnum()

    def OnCreateNewProject(self):
        #Check si le nom du projet est vide
        if self.var_name.get() == "":
            self.ShowError(LanguageSystem.GetText("Erreur"), LanguageSystem.GetText("Le nom du projet ne peut pas être vide"))
            return
        #Check si le path du projet est vide
        if self.var_path.get() == "":
            self.ShowError(LanguageSystem.GetText("Erreur"), LanguageSystem.GetText("Le path du projet ne peut pas être vide"))
            return
        #check si le nom du projet est valide
        if not self.IsValidName(self.var_name.get()):
            self.ShowError(LanguageSystem.GetText("Erreur"), LanguageSystem.GetText("Le nom du projet n'est pas valide"))
            return
        #Check si le path du projet existe
        if not os.path.exists(self.var_path.get()):
            self.ShowError(LanguageSystem.GetText("Erreur"), LanguageSystem.GetText("Le path du projet n'existe pas"))
            return
        #Check si le path du projet est un dossier
        if not os.path.isdir(self.var_path.get()):
            self.ShowError(LanguageSystem.GetText("Erreur"), LanguageSystem.GetText("Le path du projet n'est pas un dossier"))
            return
        #Check si path+nom existe deja
        if os.path.exists(os.path.join(self.var_path.get(), self.var_name.get())):
            self.ShowError(LanguageSystem.GetText("Erreur"), LanguageSystem.GetText("Le path du projet existe déjà"))
            return
        self.CreateNewProject(self.var_name.get(), self.var_path.get(), "default")
    
    def CreateNewProject(self, name, path, template):
        #creer le dossier du projet
        path = os.path.join(path, name)
        #mettre le path en absolu
        path = os.path.abspath(path)
        os.mkdir(path)
        os.mkdir(os.path.join(path, "Assets"))
        os.mkdir(os.path.join(path, "Assets", "Scripts"))
        os.mkdir(os.path.join(path, "Assets", "Textures"))
        os.mkdir(os.path.join(path, "Assets", "Scenes"))
        os.mkdir(os.path.join(path, "Library"))
        os.mkdir(os.path.join(path, "Library", "tmp"))
        os.mkdir(os.path.join(path, "Build"))
        projetConfig = {
            "name": name,
            "projectPath": path,
            "template": template,
            "language":"fr",
            "version":GlobalVars.Particle.version,
            "lastOpened": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "scene": "",
        }
        with open(os.path.join(path , "config.proj"), "w", encoding="utf-8") as f:
            json.dump(projetConfig, f, indent=4)
        self.config["projects"].append(projetConfig)
        self.SaveHubConfig()
        
        #oublier une fenetre principale (pack_forget) et repack la nouvelle fenetre
        self.NewProject_frame.pack_forget()
        self.main_frame.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        self.ShowListProjects()

    def OnAddProject(self):
        #ouvrir une fenetre pour choisir le path (dossier)
        path = tkinter.filedialog.askdirectory()
        if path:
            #check si le path+config.proj existe
            if not os.path.exists(os.path.join(path, "config.proj")) or not os.path.isfile(os.path.join(path, "config.proj")):
                self.ShowError(LanguageSystem.GetText("Erreur"), LanguageSystem.GetText("Ce repertoire n'est pas un projet"))
                return
            try:
                with open(os.path.join(path, "config.proj"), "r", encoding="utf-8") as f:
                    config = json.load(f)
            except:
                self.ShowError(LanguageSystem.GetText("Erreur"), LanguageSystem.GetText("Ce repertoire n'est pas un projet"))
                return
            #check si le path du projet existe deja
            for i in self.config["projects"]:
                if i["projectPath"] == config["projectPath"]:
                    #le faire remonter dans la liste (le mettre en premier)
                    self.config["projects"].remove(i)
                    self.config["projects"].insert(0, i)
                    
            #actualiser le path du projet dans le config
            config["projectPath"] = path
            self.Particle.SaveConfig(config)
            self.config["projects"].append(config)
            self.SaveHubConfig()
            self.ShowListProjects()

    def cancelNewProject(self):
        #oublier une fenetre principale (pack_forget) et repack la nouvelle fenetre
        self.NewProject_frame.pack_forget()
        self.main_frame.pack(fill=tkinter.BOTH, expand=tkinter.YES)

    def OnSelectEmplacementNewProject(self):
        #ouvrir une fenetre pour choisir le path
        folder = tkinter.filedialog.askdirectory()
        if folder:
            self.var_path.set(folder)

    def ChangeTab(self, tab):
        #oublier tout les content frame et repack le bon
        self.content_frame_Projets.grid_forget()
        buttons =[self.sidebar_button_1, self.sidebar_button_2, self.sidebar_button_3, self.sidebar_button_4]
        for i in buttons:
            i.configure(fg_color="transparent")
        buttons[tab-1].configure(fg_color=("gray75", "gray25"))
        if tab == 1:
            self.content_frame_Projets.grid(row=0, column=1, rowspan=4, sticky="nsew")
            

    def on_closing(self):
        self.SaveHubConfig()
        self.Particle.config = None
        self.window.destroy()
        exit()

    def ShowListProjects(self):
        self.projectsList = self.config.get("projects")
        #clear scrollable frame
        for widget in self.scrollable_frameProjet.winfo_children():
            widget.destroy()
        #load projects
        for project in self.projectsList:
            #create frame
            self.projectFrame = ctk.CTkFrame(self.scrollable_frameProjet, corner_radius=0)
            self.projectFrame.pack(fill=tkinter.X, padx=20, pady=10)
            #create label
            self.projectLabel = ctk.CTkLabel(self.projectFrame, text=project.get("name"))
            self.projectLabel.pack(side=tkinter.LEFT, padx=20, pady=10)
            #create button
            self.projectButton = ctk.CTkButton(self.projectFrame, text=LanguageSystem.GetText("Ouvrir"),
                                               command=partial(self.OnOpenProject, project.get("projectPath")))
            self.projectButton.pack(side=tkinter.RIGHT, padx=20, pady=10)
            #create button
            self.projectButton = ctk.CTkButton(self.projectFrame, text=LanguageSystem.GetText("Supprimer"), command=partial(self.OnRemoveProject, project))
            self.projectButton.pack(side=tkinter.RIGHT, padx=20, pady=10)
            #create label pour le path (afficher le path en dessous du nom)
            self.projectLabelPath = ctk.CTkLabel(self.projectFrame, text=project.get("projectPath"))
            self.projectLabelPath.pack(side=tkinter.LEFT, padx=20, pady=10)
            CreateToolTip(self.projectLabelPath, project.get("projectPath"))
        #update fit canvas
        def update_scrollregion():
            ctk.ScalingTracker.update_scaling_callbacks_for_window(self.window)
        self.window.after(500, update_scrollregion)

    def OnRemoveProject(self, project):
        self.config["projects"].remove(project)
        self.SaveHubConfig()
        self.ShowListProjects()

    def OnOpenProject(self, projectPath):
        #ouvrir le projet
        config = None
        try:
            with open(os.path.join(projectPath, "config.proj"), "r", encoding="utf-8") as f:
                config = json.load(f)
        except:
            self.ShowError(LanguageSystem.GetText("Erreur"), LanguageSystem.GetText("Ce repertoire n'est pas un projet"))
            return
        self.Particle.config = config
        #quitte le hub
        self.window.destroy()