import tkinter as tk
from tkinter import ttk 
import customtkinter as ctk

class MyToggledFrame(ctk.CTkFrame):

    def __init__(self, parent, text="", *args, **options):
        ctk.CTkFrame.__init__(self, parent, *args, **options)

        self.show = tk.IntVar()
        self.show.set(0)

        self.title_frame = ctk.CTkFrame(self)
        self.title_frame.pack(fill="x", expand=1)

        ctk.CTkLabel(self.title_frame, text=text).pack(side="left", fill="x", expand=1)

        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text='+', command=self.toggle,
                                            variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        self.sub_frame = ctk.CTkFrame(self)#, relief="sunken", borderwidth=1)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')

    def Open(self):
        self.show.set(1)
        self.toggle()

    def Close(self):
        self.show.set(0)
        self.toggle()

#exemple :
#t = MyToggledFrame(root, text='Rotate', relief="raised", borderwidth=1)
#t.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
#ttk.Label(t.sub_frame, text='Rotation [deg]:').pack(side="left", fill="x", expand=1)
#ttk.Entry(t.sub_frame).pack(side="left")