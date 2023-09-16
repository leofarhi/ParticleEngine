import tkinter as tk
import customtkinter as ctk

class MyTabview(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.ORG_set_grid_segmented_button = self._set_grid_segmented_button
        self._set_grid_segmented_button = lambda: (self.ORG_set_grid_segmented_button(),self._segmented_button.grid(padx=0, rowspan=1,sticky="nsw"))