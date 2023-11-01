#!/usr/bin/env python3.10
import os,sys
import subprocess
import platform

if platform.system() == "Windows":
    pythonCMD = ["py","-3.10"]
else:
    pythonCMD = ["python3.10"]

url = "https://github.com/leofarhi/ParticuleEngine.git"

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
os.chdir(os.path.dirname(os.path.abspath(__file__))+ "/ParticuleEngine")

#check if the folder venv exist
if os.path.isdir("venv"):
    print("You already installed Particule")

#check if the user have python 3.10
if sys.version_info[0] != 3 or sys.version_info[1] != 10:
    print("You need to have Python 3.10 to run this program")
    print("Please install Python 3.10 and try again")
    print("If you have Python 3.10 installed, please make sure that you are running this program with Python 3.10")
    input("Press enter to continue...")
    sys.exit()
    
#create the virtual environment
subprocess.run(pythonCMD+["-m", "venv", "venv"])

requirement = """
customtkinter
PyOpenGL
pyopengltk
Pillow
numpy
javalang
packaging
"""

if platform.system() == "Windows":
    requirement += """
pywin32
"""
else:
    requirement += """
"""

if platform.system() == "Windows":
    pythonCMD = ["venv\\Scripts\\python.exe"]
else:
    pythonCMD = ["venv/bin/python3"]

#install the requirements
subprocess.run(pythonCMD+["-m", "pip", "install", "--upgrade", "pip"])
for package in requirement.split("\n"):
    if package != "":
        subprocess.run(pythonCMD+["-m", "pip", "install", package])

#make Start File executable .bat for Windows and .sh for Linux
if platform.system() == "Windows":
    with open("ParticuleEngine.bat", "w") as file:
        file.write("venv\\Scripts\\python.exe main.py")
        #wait for the user to press enter
        file.write("\npause")
else:
    with open("ParticuleEngine.sh", "w") as file:
        file.write("venv/bin/python3 main.py")
        file.write("\nread -p \"Press enter to continue...\"")
    subprocess.run(["chmod","+x","./ParticuleEngine.sh"])

#wait for the user to press enter
input("Press enter to continue...")
