"""
import Parser.Parser as Parser

content = Parser.Parse(Parser.ParseFile("ProjetTests/test.py"))
if True:
    print(content.GetCFile())
    print('$'*20)
    print(content.GetHFile())
exit()
"""
__author__ = 'Farhi'
import os
import time
import shutil
import platform
import Particle.Particle as Particle
import Particle.Modules.Directory as Directory

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