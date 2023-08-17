from Particule.Modules.CallBacksSystem import *
import platform
import subprocess
import webbrowser
from math import *
import os
import time
import shutil
import sys
from tkinter import *
import tkinter
from tkinter.messagebox import *
from tkinter import messagebox
import tkinter.simpledialog
from tkinter.filedialog import *
from tkinter import ttk
import customtkinter as ctk
from customtkinter.windows.widgets.appearance_mode.appearance_mode_base_class import CTkAppearanceModeBaseClass
from customtkinter.windows.widgets.scaling.scaling_base_class import CTkScalingBaseClass
from customtkinter.windows.widgets.scaling.scaling_tracker import ScalingTracker

from OpenGL import GL

from pyopengltk import OpenGLFrame
import datetime
from PIL import Image
from PIL import ImageTk
import numpy as np
#import pylab as pl
#import matplotlib.cm as cm
#import cv2
from functools import partial
#from shutil import move
#from glob import glob
#from inspect import isclass
import importlib
#from pkgutil import iter_modules
#import pkgutil
#from pathlib import Path
#from importlib import import_module
from PIL import ImageFilter, ImageOps
#import pyglet
import json
import uuid
from enum import Enum
from Particule.Modules.MyCustomTkinter.MyPanedWindow import MyPanedWindow
from Particule.Modules.MyCustomTkinter.MyTabview import MyTabview
from Particule.Modules.MyCustomTkinter.MyTreeview import MyTreeview
from Particule.Modules.MyCustomTkinter.MyToolTip import MyToolTip,CreateToolTip

class GlobalVars:
    Particule = None