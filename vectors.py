import math

class Vector2D(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def toTuple(self):
        return (self.x, self.y)
        
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def magnitudeSquared(self):
        return self.x**2 + self.y**2

    def __add__(self, rhs):
        return Vector2D(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs):
        return Vector2D(self.x - rhs.x, self.y - rhs.y)

    def __neg__(self, rhs):
        return Vector2D(-self.x, -self.y)

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
            return False

    def copy(self):
        return Vector2D(self.x, self.y)
