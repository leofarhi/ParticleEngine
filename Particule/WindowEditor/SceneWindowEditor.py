from Particule.Modules.Includes import *
from Particule.WindowEditor.WindowEditor import WindowEditor
from Particule.Modules.LanguageSystem import LanguageSystem
from Particule.Modules.Directory import *
from Particule.Modules.Screen import GetScreenSize

class AppOgl(OpenGLFrame):

    def initgl(self):
        """Initalize gl states when the frame is created"""
        GL.glViewport(0, 0, self.width, self.height)
        GL.glClearColor(0.0, 1.0, 0.0, 0.0)    
        self.start = time.time()
        self.nframes = 0

    def redraw(self):
        """Render a single frame"""
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        tm = time.time() - self.start
        self.nframes += 1
        #print("fps",self.nframes / tm, end="\r" )

class SceneWindowEditor(WindowEditor):
    def __init__(self, master=None):
        super().__init__(master,"Scene")
        screen_size = GetScreenSize()
        self.SetSize(screen_size[0]//2, screen_size[1]//2)
        
        app = AppOgl(self.window, width=320, height=200)
        app.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        app.animate = 1
        app.after(100, app.printContext)