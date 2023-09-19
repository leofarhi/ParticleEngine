import tkinter as tk
from tkinter import ttk 
import customtkinter as ctk

class MyToggledFrame(ctk.CTkFrame):

    def __init__(self, parent, text="", *args, **options):
        ctk.CTkFrame.__init__(self, parent,border_width=2, *args, **options)

        self.show = False
        self.ButtonText = tk.StringVar()
        self.ButtonText.set("+")

        self.title_frame = ctk.CTkFrame(self,bg_color="transparent",border_width=2)
        self.title_frame.pack(fill="x", expand=1, pady=2, padx=2)

        self.toggle_button = ctk.CTkButton(self.title_frame, width=30, textvariable=self.ButtonText, command=self.toggle,bg_color="transparent")
        self.toggle_button.pack(side="left", pady=5, padx=5)

        ctk.CTkLabel(self.title_frame, text=text,bg_color="transparent").pack(side="left", fill="x", expand=1, pady=5, padx=5)

        self.sub_frame = ctk.CTkFrame(self,bg_color="transparent",border_width=2)

    def toggle(self, show=None):
        if show == None:
            self.show = not self.show
            show = self.show
        if show:
            self.sub_frame.pack(fill="x", expand=1, pady=2, padx=2)
            self.ButtonText.set("-")
        else:
            self.sub_frame.forget()
            self.ButtonText.set("+")

    def Open(self):
        self.show = True
        self.toggle(self.show)

    def Close(self):
        self.show = False
        self.toggle(self.show)

#exemple :
#t = MyToggledFrame(root, text='Rotate', relief="raised", borderwidth=1)
#t.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
#ttk.Label(t.sub_frame, text='Rotation [deg]:').pack(side="left", fill="x", expand=1)
#ttk.Entry(t.sub_frame).pack(side="left")