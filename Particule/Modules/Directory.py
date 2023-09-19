import platform
from Particule.Modules.Includes import *

def CreateDir(rep):
    os.makedirs(rep, exist_ok=True)
def DeleteDir(rep):
    shutil.rmtree(rep)
def GetAppData():
    if platform.system()=="Windows":
        rep_AppData=str(os.getenv('APPDATA'))
    elif platform.system()=="Darwin":
        rep_AppData=str(os.getenv('HOME'))+"/Library/Application Support"
    elif platform.system()=="Linux":
        rep_AppData=str(os.getenv('HOME'))+"/.local/share"
    return rep_AppData