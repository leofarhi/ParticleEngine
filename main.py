__author__ = 'Farhi'
import os, sys
import time
import shutil
import platform
import Particle.Particle as Particle
import Particle.Modules.Directory as Directory


#set working directory to the directory of the script
os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    shutil.rmtree(os.getcwd() + "/lib/tmp")
except:
    if platform.system()=="Windows":
        os.system('rmdir /S /Q "{}"'.format(os.getcwd() + "/lib/tmp"))
time.sleep(1)
Directory.CreateDir(os.getcwd() + "/lib/tmp")

Particle =  Particle.Particle()
Particle.HubWindow()
if Particle.config != None:
    Particle.Start()