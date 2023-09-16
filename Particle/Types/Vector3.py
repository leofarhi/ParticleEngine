import math
class Vector3:
    def __init__(self, x=0, y=0, z=0):
        if type(x).__name__ == "Vector2":
            self.x = x.x
            self.y = x.y
            self.z = y
            return
        self.x = x
        self.y = y
        self.z = z

    def get(self):
        return (self.x, self.y, self.z)
    
    def set(self, _tuple):
        self.x, self.y, self.z = _tuple
        return self
    
    def __str__(self):
        return str((self.x, self.y, self.z))
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other):
        return Vector3(self.x * other, self.y * other, self.z * other)
    
    def __truediv__(self, other):
        return Vector3(self.x / other, self.y / other, self.z / other)
    
    def __floordiv__(self, other):
        return Vector3(self.x // other, self.y // other, self.z // other)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __ne__(self, other):
        return not (self.x == other.x and self.y == other.y and self.z == other.z)
    
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        
        raise IndexError("Vector3 index out of range")
    
    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            self.z = value
        
        raise IndexError("Vector3 index out of range")
    
    def __len__(self):
        return 3
    
    def __iter__(self):
        return iter((self.x, self.y, self.z))
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    
    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)
    
    def __pos__(self):
        return Vector3(self.x, self.y, self.z)
    
    def __abs__(self):
        return Vector3(abs(self.x), abs(self.y), abs(self.z))
    
    def __round__(self, n=None):
        return Vector3(round(self.x, n), round(self.y, n), round(self.z, n))
    
    def __floor__(self):
        return Vector3(math.floor(self.x), math.floor(self.y), math.floor(self.z))
    
    def __ceil__(self):
        return Vector3(math.ceil(self.x), math.ceil(self.y), math.ceil(self.z))
    
    def __trunc__(self):
        return Vector3(math.trunc(self.x), math.trunc(self.y), math.trunc(self.z))
    
    def __pow__(self, other):
        return Vector3(self.x ** other, self.y ** other, self.z ** other)
    
    def __copy__(self):
        return Vector3(self.x, self.y, self.z)
    
    def __deepcopy__(self, memo):
        return Vector3(self.x, self.y, self.z)
    
    def __getstate__(self):
        return (self.x, self.y, self.z)
    
    def __setstate__(self, state):
        self.x, self.y, self.z = state
        