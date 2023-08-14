from tkinter import PanedWindow, Frame, BOTH
import customtkinter as ctk
from customtkinter.windows.widgets.appearance_mode.appearance_mode_base_class import CTkAppearanceModeBaseClass
from customtkinter.windows.widgets.scaling import CTkScalingBaseClass

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict
from typing import Union, Callable, Tuple

class MyPanedWindow(PanedWindow,CTkAppearanceModeBaseClass):
    def __init__(self, master, orient, **kwargs):
        super().__init__(master, orient=orient, **kwargs)
        CTkAppearanceModeBaseClass.__init__(self)
        self.orientation = orient

        self._bg_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]
        self.updateBGColor()

        self.MainFrames = {}

    def _set_appearance_mode(self, *args, **kwargs):
        super()._set_appearance_mode(*args, **kwargs)
        self.updateBGColor()

    def updateBGColor(self):
        PanedWindow.config(self,bg=self._apply_appearance_mode(self._bg_color))

    def SplitFrame(self,*args,**kwargs):
        frame = Frame(self)
        frame.pack(fill=BOTH, expand=True)
        frame2 = ctk.CTkFrame(frame,corner_radius=0)
        frame2.pack(fill=BOTH, expand=True)
        self.add(frame, **kwargs)
        self.MainFrames[frame2] = frame
        return frame2
    
    def GetSizeFrame(self,frame):
        return self.MainFrames[frame].winfo_width(),self.MainFrames[frame].winfo_height()