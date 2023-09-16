import math
class Vector2:
    def __init__(self, x=0, y=0):
        if type(x).__name__ == "Vector3":
            self.x = x.x
            self.y = x.y
            return
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vector2(self.x / other, self.y / other)

    def __floordiv__(self, other):
        return Vector2(self.x // other, self.y // other)

    def __mod__(self, other):
        return Vector2(self.x % other, self.y % other)

    def __pow__(self, other):
        return Vector2(self.x ** other, self.y ** other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y

    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y

    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y

    def __str__(self):
        return f"Vector2({self.x}, {self.y})"

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value

    def __len__(self):
        return 2

    def __hash__(self):
        return hash((self.x, self.y))

    def __neg__(self):
        return Vector2(-self.x, -self.y)
    
    def __pos__(self):
        return Vector2(self.x, self.y)
    
    def __abs__(self):
        return Vector2(abs(self.x), abs(self.y))
    
    def __round__(self, n=None):
        return Vector2(round(self.x, n), round(self.y, n))
    
    def __floor__(self):
        return Vector2(math.floor(self.x), math.floor(self.y))
    
    def __ceil__(self):
        return Vector2(math.ceil(self.x), math.ceil(self.y))
    
    def __copy__(self):
        return Vector2(self.x, self.y)
    
    def __deepcopy__(self, memo):
        return Vector2(self.x, self.y)
    
    def __getstate__(self):
        return (self.x, self.y)
    
    def __setstate__(self, state):
        self.x, self.y = state