from tkinter import ttk
import customtkinter as ctk
from customtkinter.windows.widgets.appearance_mode.appearance_mode_base_class import CTkAppearanceModeBaseClass

class MyTreeview(ttk.Treeview, CTkAppearanceModeBaseClass):
    def __init__(self, master, **kwargs):
        self.style = ttk.Style()
        ttk.Treeview.__init__(self,master, **kwargs)
        CTkAppearanceModeBaseClass.__init__(self)
        self.updateStyle()

    def updateStyle(self):
        bg_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        selected_text_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["text_color"])
        self.style.theme_use('default')
        self.style.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0)
        self.style.map('Treeview', background=[('selected', selected_color)], foreground=[('selected', selected_text_color)])
        self.style.configure("Treeview.Heading", background=bg_color, foreground=text_color, borderwidth=0)
        self.style.map('Treeview.Heading', background=[('selected', selected_color)], foreground=[('selected', selected_text_color)])
        self.style.configure("Treeview.Item", background=bg_color, foreground=text_color, borderwidth=0)
        self.style.map('Treeview.Item', background=[('selected', selected_color)], foreground=[('selected', selected_text_color)])
        self.style.configure("Treeview.Cell", background=bg_color, foreground=text_color, borderwidth=0)
        self.style.map('Treeview.Cell', background=[('selected', selected_color)], foreground=[('selected', selected_text_color)])
        self.style.configure("Treeview.Row", background=bg_color, foreground=text_color, borderwidth=0)
        self.style.map('Treeview.Row', background=[('selected', selected_color)], foreground=[('selected', selected_text_color)])
        self.style.configure("Treeview.Column", background=bg_color, foreground=text_color, borderwidth=0)
        self.style.map('Treeview.Column', background=[('selected', selected_color)], foreground=[('selected', selected_text_color)])
        #font size
        self.style.configure("Treeview", font=(None, 12))
        
    def _set_appearance_mode(self, *args, **kwargs):
        super()._set_appearance_mode(*args, **kwargs)
        self.updateStyle()