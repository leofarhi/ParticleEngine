__author__ = 'Farhi'
import os, sys
import time
import shutil
import platform
import Particule.Particule as Particule
import Particule.Modules.Directory as Directory


#set working directory to the directory of the script
os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    shutil.rmtree(os.getcwd() + "/lib/tmp")
except:
    if platform.system()=="Windows":
        os.system('rmdir /S /Q "{}"'.format(os.getcwd() + "/lib/tmp"))
time.sleep(1)
Directory.CreateDir(os.getcwd() + "/lib/tmp")

Particule =  Particule.Particule()
Particule.HubWindow()
if Particule.config != None:
    Particule.Start()