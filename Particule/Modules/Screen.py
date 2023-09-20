import platform
import subprocess

if platform.system()=="Windows":
    from win32api import GetSystemMetrics
    def GetScreenSize():
        return (GetSystemMetrics(0),GetSystemMetrics(1))
elif platform.system()=="Darwin":
    from AppKit import NSScreen
    def GetScreenSize():
        return (NSScreen.mainScreen().frame().size.width,NSScreen.mainScreen().frame().size.height)
elif platform.system()=="Linux":
    def GetScreenSize():
        return tuple(map(int, subprocess.check_output(['xrandr', '--current']).split(b'primary')[1].split(b"+")[0].split()[0].split(b'x')))
else:
    def GetScreenSize():
        return (500,500)