import os, sys
currentWorkingDirectory = os.getcwd()
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))
import javalang

from Base import BaseNode
from Content import Content
import importlib

### Redirection
def LoadLanguage(name):
    Nodes = dict()
    for i in os.listdir(os.path.dirname(__file__) + "/Nodes"):
        if i.endswith(".py"):
            if i != "__init__.py":
                mod = importlib.import_module("Nodes." + i[:-3])
                modClass = getattr(mod, i[:-3])
                Nodes[i[:-3]] = modClass
    for i in Nodes:
        Nodes[i].RegisterNodes = Nodes
    BaseNode.RegisterNodes = Nodes
    path = os.path.dirname(__file__) + "/Language"
    if name in os.listdir(path):
        for i in os.listdir(path+"/"+name+"/Nodes"):
            if i.endswith(".py"):
                if i != "__init__.py":
                    mod = importlib.import_module("Language." + name + ".Nodes." + i[:-3])
                    modClass = getattr(mod, i[:-3])
                    Nodes[i[:-3]] = modClass
        for i in Nodes:
            Nodes[i].RegisterNodes = Nodes
        BaseNode.RegisterNodes = Nodes
### End Redirection

LoadLanguage(None)

def Parse(filename):
    with open(filename, "r") as f:
        text = f.read()
    tree = javalang.parse.parse(text)
    file = BaseNode.NewNode("NodeFile")("file.java",tree)
    file.Compile()
    return file

if __name__ == "__main__":
    content = Parse(os.path.dirname(__file__) +"/JavaTextTest.java").GetContent()

os.chdir(currentWorkingDirectory)
sys.path.remove(os.path.dirname(__file__))