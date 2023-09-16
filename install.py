#!/usr/bin/env python3.10
import os,sys
import subprocess
import platform

url = "https://github.com/leofarhi/ParticleEngine.git"

#check if the user have git installed with the command git
try:
    subprocess.run(["git", "--version"])
except FileNotFoundError:
    print("You need to have git installed to run this program")
    print("Please install git and try again")
    input("Press enter to continue...")
    sys.exit()

#check if the user have git installed with the command git
try:
    subprocess.run(["git", "clone", url])
except:
    print("You need to have git installed to run this program")
    print("Please install git and try again")
    input("Press enter to continue...")
    sys.exit()

#set this folder as the current working directory
os.chdir(os.path.dirname(os.path.abspath(__file__))+ "/ParticleEngine")

#check if the folder venv exist
if os.path.isdir("venv"):
    print("You already installed Particle")

#check if the user have python 3.10
if sys.version_info[0] != 3 or sys.version_info[1] != 10:
    print("You need to have Python 3.10 to run this program")
    print("Please install Python 3.10 and try again")
    print("If you have Python 3.10 installed, please make sure that you are running this program with Python 3.10")
    input("Press enter to continue...")
    sys.exit()

#check if the user have pip
try:
    import pip
except ImportError:
    print("You need to have pip to run this program")
    print("Please install pip and try again")
    input("Press enter to continue...")
    
#create the virtual environment
subprocess.run(["py","-3.10", "-m", "venv", "venv"])

requirement = """
customtkinter
PyOpenGL
pyopengltk
Pillow
numpy
javalang
"""

if platform.system() == "Windows":
    requirement += """
pywin32
"""
else:
    requirement += """
"""

#install the requirements
subprocess.run(["venv\\Scripts\\python.exe", "-m", "pip", "install", "--upgrade", "pip"])
for package in requirement.split("\n"):
    if package != "":
        subprocess.run(["venv\\Scripts\\python.exe", "-m", "pip", "install", package])

#make Start File executable .bat for Windows and .sh for Linux
if platform.system() == "Windows":
    with open("ParticleEngine.bat", "w") as file:
        file.write("venv\\Scripts\\python.exe main.py")
        #wait for the user to press enter
        file.write("\npause")
else:
    with open("ParticleEngine.sh", "w") as file:
        file.write("venv/bin/python3.10 main.py")
        file.write("\nread -p \"Press enter to continue...\"")

#wait for the user to press enter
input("Press enter to continue...")