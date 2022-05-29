from math import sqrt

class SimpleLocation:
    """Class representing a location. It contains:
        -the x coordinate: float
        -the y coordinate: float
        -the z coordinate: float
    """
    def __init__(self, x: float, y: float, z: float) -> None:
        """Init the SimpleLocation"""
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self,location):
        """Compare this SimpleLocation and another.
            :return: the comparaison's result
        """
        return self.x == location.x and self.y == location.y and self.z == location.z
    
    def distance(self, loc):
        """Compute and return the distance between this SimpleLocation and another"""
        return sqrt(pow(self.x - loc.x, 2)+pow(self.y - loc.y, 2)+pow(self.z - loc.z, 2))
