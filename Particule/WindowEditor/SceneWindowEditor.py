from Particule.Modules.Includes import *
from Particule.WindowEditor.WindowEditor import WindowEditor
from Particule.Modules.LanguageSystem import LanguageSystem
from Particule.Modules.Directory import *
from Particule.Modules.Screen import GetScreenSize

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

vertices = (
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
)
edges = ((0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7), (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7))
surfaces = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4), (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6))
colors = ((1, 0, 0), (0, 1, 0), (1, 0.5, 0), (1, 1, 0), (1, 1, 1), (0, 0, 1))

rot_cube_map = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}

class Cube():
    def __init__(self, id, N, scale):
        self.N = 3
        self.scale = scale
        self.init_i = [*id]
        self.current_i = [*id]
        self.rot = [[1 if i == j else 0 for i in range(3)] for j in range(3)]

    def isAffected(self, axis, slice, dir):
        return self.current_i[axis] == slice

    def update(self, axis, slice, dir):

        if not self.isAffected(axis, slice, dir):
            return

        i, j = (axis + 1) % 3, (axis + 2) % 3
        for k in range(3):
            self.rot[k][i], self.rot[k][j] = -self.rot[k][j] * dir, self.rot[k][i] * dir

        self.current_i[i], self.current_i[j] = (
            self.current_i[j] if dir < 0 else self.N - 1 - self.current_i[j],
            self.current_i[i] if dir > 0 else self.N - 1 - self.current_i[i])

    def transformMat(self):
        scaleA = [[s * self.scale for s in a] for a in self.rot]
        scaleT = [(p - (self.N - 1) / 2) * 2.1 * self.scale for p in self.current_i]
        return [*scaleA[0], 0, *scaleA[1], 0, *scaleA[2], 0, *scaleT, 1]

    def draw(self, col, surf, vert, animate, angle, axis, slice, dir):

        glPushMatrix()
        if animate and self.isAffected(axis, slice, dir):
            glRotatef(angle * dir, *[1 if i == axis else 0 for i in range(3)])
        glMultMatrixf(self.transformMat())

        glBegin(GL_QUADS)
        for i in range(len(surf)):
            glColor3fv(colors[i])
            for j in surf[i]:
                glVertex3fv(vertices[j])
        glEnd()

        glPopMatrix()


class mycube():
    def __init__(self, N, scale):
        self.N = N
        cr = range(self.N)
        self.cubes = [Cube((x, y, z), self.N, scale) for x in cr for y in cr for z in cr]

    def maindd(self):
        for cube in self.cubes:
            cube.draw(colors, surfaces, vertices, False, 0, 0, 0, 0)

class GLFrame(OpenGLFrame):
    def initgl(self):
        self.animate = True
        self.rota = 0
        self.count = 0

        self.ang_x, self.ang_y, self.rot_cube = 0, 0, (0, 0)
        self.action = (0, 0, 0)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        # glViewport(400, 400, 200, 200)

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)

        glMatrixMode(GL_PROJECTION)  
        glLoadIdentity()
        gluPerspective(30, self.width / self.height, 0.1, 50.0)

        self.N = 3
        cr = range(self.N)
        self.cubes = [Cube((x, y, z), self.N, 1.5) for x in cr for y in cr for z in cr]

    def keydown(self, event):
        if event.keysym in rot_cube_map:
            self.rot_cube = rot_cube_map[event.keysym]

    def keyup(self, event):
        if event.keysym in rot_cube_map:
            self.rot_cube = (0, 0)

    def redraw(self):
        self.ang_x += self.rot_cube[0] * 2
        self.ang_y += self.rot_cube[1] * 2

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -40)
        glRotatef(self.ang_y, 0, 1, 0)
        glRotatef(self.ang_x, 1, 0, 0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for cube in self.cubes:
            cube.draw(colors, surfaces, vertices, self.animate, 0, *self.action)

class SceneWindowEditor(WindowEditor):
    def __init__(self, master=None):
        super().__init__(master,"Scene")
        screen_size = GetScreenSize()
        self.SetSize(screen_size[0]//2, screen_size[1]//2)
        self.glframe = GLFrame(self.window, width=800, height=600)
        self.OnFocus = False
        self.Particule.window.bind("<KeyPress>", lambda event: self.Remote(event,"<KeyPress>"))
        self.Particule.window.bind("<KeyRelease>", lambda event: self.Remote(event,"<KeyRelease>"))
        self.Particule.window.bind("<Button-1>", lambda event: self.Remote(event,"<Button-1>"))
        self.glframe.pack(expand=True, fill=BOTH)

    def Remote(self,event,bindName):
        if bindName == "<Button-1>":
            self.OnFocus = event.widget == self.glframe
            if self.OnFocus:
                self.glframe.focus_set()
                self.glframe.focus_force()
            return
        if bindName == "<KeyRelease>":
            self.glframe.keyup(event)
            return
        if not self.OnFocus:
            return
        if bindName == "<KeyPress>":
            self.glframe.keydown(event)
            return
    
    @AddCallBackToStack("OnCreateMenu", 0)
    def OnCreateMenu():
        GlobalVars.Particule.AddCommandsMenu("File", {
            "Nouvelle Scene": (),
            "Ouvrir une Scene": (),
            "Ouvrir une Scene recente": (),
        },False)
        def SaveScene():
            if GlobalVars.Particule.sceneManager.CurrentScene is not None:
                GlobalVars.Particule.sceneManager.CurrentScene.Save()
        def SaveSceneAs():
            #open file dialog
            path = tkinter.filedialog.asksaveasfilename(initialdir=GlobalVars.Particule.config.get("projectPath"),title="Enregistrer la Scene sous",filetypes=(("Scene","*.scene"),("Tous les fichiers","*.*")))
            if path != "":
                if os.path.splitext(path)[1] != ".scene":
                    path += ".scene"
                GlobalVars.Particule.sceneManager.CurrentScene.Save(path)
        GlobalVars.Particule.AddCommandsMenu("File", {
            "Enregistrer la Scene": SaveScene,
            "Enregistrer la Scene sous": SaveSceneAs,
        }, True)