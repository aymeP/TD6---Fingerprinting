from math import sqrt

class SimpleLocation:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self,location):
        return self.x == location.x and self.y == location.y and self.z == location.z
    
    def distance(self, loc):
        return sqrt(pow(self.x - loc.x, 2)+pow(self.y - loc.y, 2)+pow(self.z - loc.z, 2))
