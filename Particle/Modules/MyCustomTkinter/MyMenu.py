
from tkinter import ttk
import customtkinter as ctk
from customtkinter.windows.widgets.appearance_mode.appearance_mode_base_class import CTkAppearanceModeBaseClass
from tkinter import Menu
from Particle.Modules.LanguageSystem import LanguageSystem

class MyMenu(Menu, CTkAppearanceModeBaseClass):
    def __init__(self, master):
        Menu.__init__(self,master, tearoff=0)
        self.subsMenu = {}
        CTkAppearanceModeBaseClass.__init__(self)
        self.updateStyle()

    def _set_appearance_mode(self, *args, **kwargs):
        super()._set_appearance_mode(*args, **kwargs)
        self.updateStyle()

    def updateStyle(self):
        self.config(font= ("Arial",11))
        #change font for all items
        return
        bg_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        disabled_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["text_color_disabled"])
        selected_text_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["text_color"])
        
        self.config(bg=bg_color, fg=text_color, activebackground=selected_color, activeforeground=selected_text_color,
                    borderwidth=0, relief="flat",border=0,font= (None,12),disabledforeground=disabled_color)
        self.update()

    def AddCommand(self, pathMenu, command=()):
        nameMenu, secondPart = pathMenu.split("/", 1)
        if nameMenu not in self.subsMenu:
            self.subsMenu[nameMenu] = MyMenu(self)
            self.add_cascade(label=LanguageSystem.GetText(nameMenu), menu=self.subsMenu[nameMenu])
        if "/" in secondPart:
            self.subsMenu[nameMenu].AddCommand(secondPart, command)
        else:
            self.subsMenu[nameMenu].add_command(label=secondPart, command=command)
        self.updateStyle()

    def DisableCommand(self, pathMenu):
        nameMenu, secondPart = pathMenu.split("/", 1)
        if nameMenu not in self.subsMenu:
            self.subsMenu[nameMenu] = MyMenu(self)
            self.add_cascade(label=LanguageSystem.GetText(nameMenu), menu=self.subsMenu[nameMenu])
        if "/" in secondPart:
            self.subsMenu[nameMenu].DisableCommand(secondPart)
        else:
            self.subsMenu[nameMenu].entryconfig(secondPart, state="disabled")
        self.updateStyle()

    def EnableCommand(self, pathMenu):
        nameMenu, secondPart = pathMenu.split("/", 1)
        if nameMenu not in self.subsMenu:
            self.subsMenu[nameMenu] = MyMenu(self)
            self.add_cascade(label=LanguageSystem.GetText(nameMenu), menu=self.subsMenu[nameMenu])
        if "/" in secondPart:
            self.subsMenu[nameMenu].EnableCommand(secondPart)
        else:
            self.subsMenu[nameMenu].entryconfig(secondPart, state="normal")
        self.updateStyle()
        
    def AddSeparator(self, pathMenu):
        if "/" in pathMenu:
            nameMenu, secondPart = pathMenu.split("/", 1)
            self.subsMenu[nameMenu].AddSeparator(secondPart)
        else:
            nameMenu = pathMenu
            if nameMenu not in self.subsMenu:
                self.subsMenu[nameMenu] = MyMenu(self)
                self.add_cascade(label=LanguageSystem.GetText(nameMenu), menu=self.subsMenu[nameMenu])
            self.subsMenu[nameMenu].add_separator()
        self.updateStyle()