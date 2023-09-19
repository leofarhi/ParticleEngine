import Parser.Parser as Parser
import os, sys
from Particle.Modules.Includes import *
from Parser.Language.Python.Types import *
import importlib.util
import importlib

class InstanceEnvironmentObject:
    def __init__(self, RegistredObject=None):
        self.__IsDestroyed__ = False
        if RegistredObject == None:
            name = self.__class__.__name__
            RegistredObject = EnvironmentSystem.Instance.Objects.get(name,None)
            if RegistredObject == None:
                raise Exception("Object not found")
            RegistredObject.SetUp(self)
            EnvironmentSystem.Instance.InstancesObjects.append(self)
        self.__class__.__name__ = RegistredObject.name
        self.__RegistredObject__ = RegistredObject

    def __reference__(self, *args, **kwargs):
        return self.__RegistredObject__.name
    
    def __setreference__(data,*args, **kwargs):
        return NewEnv(data)
    
    def getDict(self):
        dico = {}
        for attribute in self.__RegistredObject__.attributes:
            if attribute not in self.__dict__:
                self.__setattr__(attribute,self.__RegistredObject__.defautlValues[attribute])
            dico[attribute] = self.__convertValueGet__(self.__dict__[attribute],self.__RegistredObject__.typesOfAttributes[attribute])
        return dico
    
    def __convertValueGet__(self, value,type):
        if value == None:
            return None
        if type.name in RegistredObject.OverwriteObjects:
            value = value.__reference__()
        elif type.name in EnvironmentSystem.Instance.Objects:
            value = value.getDict()
        elif type.name == "ArrayList":
            value = [self.__convertValueGet__(val,type.arguments[0]) for val in value]
        return value

    def setDict(self, dict):
        for key in dict:
            if key in self.__RegistredObject__.attributes:
                value = dict[key]
                self.__setattr__(key,self.__convertValueSet__(value,self.__RegistredObject__.typesOfAttributes[key]))
                
    def __convertValueSet__(self, value,type):
        if value == None:
            return None
        if type.name in RegistredObject.OverwriteObjects:
            CLASS = RegistredObject.OverwriteObjects[type.name]
            value = CLASS.__setreference__(value)
        elif type.name in EnvironmentSystem.Instance.Objects:
            temp = NewEnv(type.name)
            temp.setDict(value)
            value = temp
        elif type.name == "ArrayList":
            value = [self.__convertValueSet__(val,type.arguments[0]) for val in value]
        return value
    
    def Destroy(self):
        self.__IsDestroyed__ = True
        for key, value in self.__dict__.items():
            if hasattr(value,"__IsDestroyed__"):
                value.__IsDestroyed__ = True

        
class RegistredObject:
    OverwriteObjects = {}
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.extend = None
        self.local_attributes = []
        self.local_defautlValues = {}
        self.local_typesOfAttributes = {}
        self.local_attributesObject = {}

    @property
    def attributes(self):
        if self.extend == None:
            return self.local_attributes
        return self.local_attributes + self.extend.attributes
    
    @property
    def defautlValues(self):
        if self.extend == None:
            return self.local_defautlValues
        return {**self.extend.defautlValues, **self.local_defautlValues}
    
    @property
    def typesOfAttributes(self):
        if self.extend == None:
            return self.local_typesOfAttributes
        return {**self.extend.typesOfAttributes, **self.local_typesOfAttributes}
    
    @property
    def attributesObject(self):
        if self.extend == None:
            return self.local_attributesObject
        return {**self.extend.attributesObject, **self.local_attributesObject}
    
    @property
    def type(self):
        return self.data.__class__.__name__
    
    def Instantiate(self,*args, **kwargs):
        CLASS = InstanceEnvironmentObject
        if self.name in RegistredObject.OverwriteObjects:
            CLASS = RegistredObject.OverwriteObjects[self.name]
        inst = CLASS(*args, **kwargs,RegistredObject=self)
        for attribute in self.attributes:
            if attribute not in inst.__dict__:
                inst.__setattr__(attribute,self.defautlValues[attribute])
        return inst
    
    def SetUp(self,inst):
        for attribute in self.attributes:
            if attribute not in inst.__dict__:
                inst.__setattr__(attribute,self.defautlValues[attribute])
    
#decorator
def OverwriteObject():
    def decorator(Class):
        RegistredObject.OverwriteObjects[Class.__name__] = Class
        return Class
    return decorator

class EnvironmentSystem:
    Instance = None
    def __init__(self,particle):
        EnvironmentSystem.Instance = self
        self.particle = particle
        self.files = []
        self.roots = [] #Roots of the files
        self.env = []
        self.Objects = {}
        self.InstancesObjects = []

        self.EditorsFiles = []#Files of the editors .py
        self.EditorsEnv = {}#Environement of the editors

    def UpdateFiles(self):
        self.files = []
        for root in self.roots:
            for path, subdirs, files in os.walk(root):
                for name in files:
                    if name.endswith(".java"):
                        self.files.append(os.path.join(path, name))
                    elif name.endswith(".py"):
                        self.EditorsFiles.append(os.path.join(path, name))
        """
        for file in self.EditorsFiles:
            filename = os.path.basename(file)
            if filename in self.EditorsEnv:
                raise Exception("Two editors with the same name")
            else:
                #importlib by full path
                spec = importlib.util.spec_from_file_location(filename, file)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                self.EditorsEnv[filename] = mod
        """

    def Compile(self):
        self.env = []
        for file in self.files:
            self.env.append(Parser.Parse(file))
        self.Objects = {}
        Temp = []
        for env in self.env:
            for obj in env.body:
                if obj.__class__.__name__ in "NodeClassDeclaration":
                    registTemp = RegistredObject(obj.name, obj)
                    self.Objects[obj.name] = registTemp
                    Temp.append((registTemp, obj))
        for item in Temp:
            registTemp, obj = item
            for attribute in obj.attributes:
                registTemp.local_attributes.append(attribute.name)
                registTemp.local_attributesObject[attribute.name] = attribute
                if attribute.defaultValue != None:
                    value = eval(TranslateValue(attribute.defaultValue))
                else:
                    NewType = TranslateType(attribute.type)
                    if NewType == None:
                        if attribute.type.name in self.Objects:
                            CLASS_OBJ = self.Objects[attribute.type.name].data
                            if CLASS_OBJ.GetAnnotation("Serializable") != None:
                                value = NewEnv(attribute.type.name)
                        else:
                            value = None
                    else:
                        value = eval(DeflautValue(NewType))
                registTemp.local_defautlValues[attribute.name] = value
                registTemp.local_typesOfAttributes[attribute.name] = attribute.type
        for value in self.Objects.values():
            if len(value.data.extends) > 0:
                value.extend = self.Objects[value.data.extends[0]]
        for inst in self.InstancesObjects:
            #check Object exist
            if inst.__RegistredObject__.name not in self.Objects:
                inst.__IsDestroyed__ = True
            else:
                #check attributes if are added => set default value
                for attribute in self.Objects[inst.__RegistredObject__.name].attributes:
                    if attribute not in inst.__dict__:
                        inst.__setattr__(attribute,self.Objects[inst.__RegistredObject__.name].defautlValues[attribute])
                    """
                    else:
                        #check type
                        #old chage this : if inst.__dict__[attribute].__class__.__name__ != self.Objects[inst.__RegistredObject__.name].typesOfAttributes[attribute]:
                            #reset value
                            inst.__setattr__(attribute,self.Objects[inst.__RegistredObject__.name].defautlValues[attribute])
                    """
        self.UpdateInstances()
    def UpdateInstances(self):
        self.InstancesObjects = [inst for inst in self.InstancesObjects if inst.__IsDestroyed__ == False]
        print(len(self.InstancesObjects))

def NewEnv(nameObject, *args, **kwargs):
    self = EnvironmentSystem.Instance
    val = self.Objects.get(nameObject,None)
    if val == None:
        raise Exception("Object not found")
    else:
        inst = val.Instantiate(*args, **kwargs)
        self.InstancesObjects.append(inst)
        return inst
    
GlobalVars.NewEnv = NewEnv