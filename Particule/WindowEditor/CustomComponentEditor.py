from Particule.Modules.Includes import *


class SerializedProperty:
    def __init__(self, obj, attributeName,type,access="$val$"):
        self.obj = obj
        self.attributeName = attributeName
        self.type = type
        self.access = access
    
    def GetValue(self):
        __val__ = getattr(self.obj,self.attributeName)
        #access ex: ($$.text)[0][1]
        access = self.access.replace("$val$","__val__")
        val = eval(access)
        return val
    
    def SetValue(self,value):
        if self.access == "$val$":
            setattr(self.obj,self.attributeName,value)
            return
        else:
            __val__ = getattr(self.obj,self.attributeName)
            #access ex: ($$.text)[0][1]
            access = self.access.replace("$val$","__val__")
            exec(access+"=value")
            setattr(self.obj,self.attributeName,__val__)

class PropertyDrawer:
    Register = {}
    def New(type):
        if type in PropertyDrawer.Register:
            return PropertyDrawer.Register[type]
        return None
    def __init__(self,masterFrame,serializedProperty):
        self.masterFrame = masterFrame
        self.serializedProperty = serializedProperty

#decorator
def CustomPropertyDrawer(type):
    def decorator(Class):
        PropertyDrawer.Register[type] = Class
        return Class
    return decorator

class ComponentDrawer:
    Register = {}
    def New(componentName):
        if componentName in ComponentDrawer.Register:
            return ComponentDrawer.Register[componentName]
        return ComponentDrawer
    def __init__(self,masterFrame,component):
        self.masterFrame = masterFrame
        self.component = component
        self.fields = {}

    @property
    def attributes(self):
        return self.component.__RegistredObject__.attributesObject
    
    @property
    def typesOfAttributes(self):
        return self.component.__RegistredObject__.typesOfAttributes

    def SerializeFields(self):
        for key,attribute in self.attributes.items():
            if attribute.GetAnnotation("HideInInspector") != None:
                continue
            TYPE = self.typesOfAttributes[key]
            CLASS = PropertyDrawer.New(TYPE.name)
            if CLASS != None:
                self.fields[key] = CLASS(self.masterFrame,SerializedProperty(self.component,key,self.typesOfAttributes[key]))

#decorator
def CustomComponentDrawer(type):
    def decorator(Class):
        ComponentDrawer.Register[type] = Class
        return Class
    return decorator


@CustomPropertyDrawer("int")
@CustomPropertyDrawer("byte")
@CustomPropertyDrawer("short")
@CustomPropertyDrawer("long")
class IntDrawer(PropertyDrawer):
    def __init__(self,masterFrame,serializedProperty):
        super().__init__(masterFrame,serializedProperty)
        self.frame = ctk.CTkFrame(self.masterFrame)
        self.frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        #config grid
        self.frame.grid_columnconfigure(1, weight=1)
        #label grid
        self.label = ctk.CTkLabel(self.frame,text=self.serializedProperty.attributeName)
        self.label.grid(row=0,column=0,padx=2)
        self.var = IntVar()
        self.var.set(self.serializedProperty.GetValue())
        self.var.trace_add("write",self.OnValueChanged)
        self.entry = ctk.CTkEntry(self.frame,textvariable=self.var)
        self.entry.grid(row=0,column=1,sticky="ew")
        self.OnValueChanged()
        self.entry.bind("<FocusOut>",self.OnFocusOut)

    def OnValueChanged(self,*args):
        try:int(float(self.var.get()))
        except:return
        if type(self.var.get())!=int:
            self.var.set(int(float(self.var.get())))
        self.serializedProperty.SetValue(self.var.get())
    
    def OnFocusOut(self,*args):
        try:self.var.get()
        except:self.var.set(0)
        self.OnValueChanged()
@CustomPropertyDrawer("float")
@CustomPropertyDrawer("double")
class FloatDrawer(PropertyDrawer):
    def __init__(self,masterFrame,serializedProperty):
        super().__init__(masterFrame,serializedProperty)
        self.frame = ctk.CTkFrame(self.masterFrame)
        self.frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        #config grid
        self.frame.grid_columnconfigure(1, weight=1)
        #label grid
        self.label = ctk.CTkLabel(self.frame,text=self.serializedProperty.attributeName)
        self.label.grid(row=0,column=0,padx=2)
        self.var = DoubleVar()
        self.var.set(self.serializedProperty.GetValue())
        self.var.trace_add("write",self.OnValueChanged)
        self.entry = ctk.CTkEntry(self.frame,textvariable=self.var)
        self.entry.grid(row=0,column=1,sticky="ew")
        self.OnValueChanged()
        self.entry.bind("<FocusOut>",self.OnFocusOut)

    def OnValueChanged(self,*args):
        try:float(self.var.get())
        except:return
        self.serializedProperty.SetValue(float(self.var.get()))

    def OnFocusOut(self,*args):
        try:self.var.get()
        except:self.var.set(0)
        self.OnValueChanged()

@CustomPropertyDrawer("boolean")
class BoolDrawer(PropertyDrawer):
    def __init__(self,masterFrame,serializedProperty):
        super().__init__(masterFrame,serializedProperty)
        self.frame = ctk.CTkFrame(self.masterFrame)
        self.frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        #label grid
        self.label = ctk.CTkLabel(self.frame,text=self.serializedProperty.attributeName)
        self.label.grid(row=0,column=0,padx=2)
        self.var = BooleanVar()
        self.var.set(self.serializedProperty.GetValue())
        self.var.trace_add("write",self.OnValueChanged)
        self.entry = ctk.CTkCheckBox(self.frame,variable=self.var,text="")
        self.entry.grid(row=0,column=1,sticky="ew")
        self.OnValueChanged()

    def OnValueChanged(self,*args):
        self.serializedProperty.SetValue(self.var.get())

@CustomPropertyDrawer("String")
class StringDrawer(PropertyDrawer):
    def __init__(self,masterFrame,serializedProperty):
        super().__init__(masterFrame,serializedProperty)
        self.frame = ctk.CTkFrame(self.masterFrame)
        self.frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        self.frame.grid_columnconfigure(1, weight=1)
        #label grid
        self.label = ctk.CTkLabel(self.frame,text=self.serializedProperty.attributeName)
        self.label.grid(row=0,column=0,padx=2)
        self.var = StringVar()
        self.var.set(self.serializedProperty.GetValue())
        self.var.trace_add("write",self.OnValueChanged)
        self.entry = ctk.CTkEntry(self.frame,textvariable=self.var)
        self.entry.grid(row=0,column=1,sticky="ew")
        #self.OnValueChanged()

    def OnValueChanged(self,*args):
        self.serializedProperty.SetValue(self.var.get())

@CustomPropertyDrawer("char")
class CharDrawer(PropertyDrawer):
    def __init__(self,masterFrame,serializedProperty):
        super().__init__(masterFrame,serializedProperty)
        self.frame = ctk.CTkFrame(self.masterFrame)
        self.frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        self.frame.grid_columnconfigure(1, weight=1)
        #label grid
        self.label = ctk.CTkLabel(self.frame,text=self.serializedProperty.attributeName)
        self.label.grid(row=0,column=0,padx=2)
        self.var = StringVar()
        self.var.set(self.serializedProperty.GetValue())
        self.var.trace_add("write",self.OnValueChanged)
        
        #validate char
        def validate(text):
            if len(text) <= 1:
                return True
            return False

        self.entry = ctk.CTkEntry(self.frame,textvariable=self.var,validate="key",validatecommand=(self.frame.register(validate), '%P'))
        self.entry.grid(row=0,column=1,sticky="ew")
        #self.OnValueChanged()

    def OnValueChanged(self,*args):
        self.serializedProperty.SetValue(self.var.get())