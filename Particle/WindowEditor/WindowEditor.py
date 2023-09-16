from Particle.Modules.Includes import *
from Particle.Modules.LanguageSystem import LanguageSystem

class WindowEditor(CTkAppearanceModeBaseClass):
    def __init__(self,master=None,title="",ToplevelClass = ctk.CTkToplevel):
        self.Particle = GlobalVars.Particle
        self.master = master
        if self.master !=None:
            CTkAppearanceModeBaseClass.__init__(self)
        self.WindowMode = None
        self.window = None
        self.title = title
        if GlobalVars.Particle.window is None:
            #make window
            self.window = ctk.CTk()
            self.window._set_appearance_mode = self._set_appearance_mode
            self.window.title(LanguageSystem.GetText(self.title))
            self.LoadWindowIcon()
            self.WindowMode = "window"
        elif master is None:
            #make toplevel window
            self.WindowMode = "toplevel"
            self.window = ToplevelClass(GlobalVars.Particle.window)
            self.window._set_appearance_mode = self._set_appearance_mode

        elif type(master) in [ctk.CTkTabview,MyTabview]:
            #make tab
            self.WindowMode = "tab"
            master.add(self.title)
            self.window = ctk.CTkFrame(master.tab(self.title))
        else:
            raise Exception("WindowEditor: master type not supported")

    def SetSize(self,width,height):
        if self.WindowMode == "window":
            self.window.geometry(str(width) + "x" + str(height))

    def Pack(self):
        if self.WindowMode == "window":
            self.window.mainloop()
        elif self.WindowMode == "toplevel":
            self.window.mainloop()
        elif self.WindowMode == "tab":
            self.window.pack(fill=tkinter.BOTH, expand=True)

    def Unpack(self):
        if self.WindowMode == "window":
            self.window.destroy()
        elif self.WindowMode == "toplevel":
            self.window.destroy()
        elif self.WindowMode == "tab":
            self.window.pack_forget()

    def Destroy(self):
        if self.WindowMode == "tab":
            self.window.destroy()
            return
        self.Unpack()

    def LoadWindowIcon(self):
        if platform.system()=="Windows":
            self.window.iconbitmap("lib/UI/Icons/icon.ico")
        elif platform.system()=="Darwin":
            self.window.iconbitmap("lib/UI/Icons/icon.xbm")
        elif platform.system()=="Linux":
            self.window.iconbitmap("lib/UI/Icons/icon.xbm")

    def _set_appearance_mode(self, *args, **kwargs):
        super()._set_appearance_mode(*args, **kwargs)
        self.OnChangeAppearanceMode(self._get_appearance_mode())

    def UpdateAppearanceMode(self):
        self.OnChangeAppearanceMode(self._get_appearance_mode()=="dark")

    def OnChangeAppearanceMode(self,mode):
        pass