from ctypes.wintypes import FLOAT
from SimpleLocation import SimpleLocation

class AccessPoint:
    def __init__(self, mac: str, x:float, y:float, z:float, f=2417000000, a=5.0, p=20.0) -> None:
        self.mac_address = mac
        self.location = SimpleLocation(x,y,z)
        self.output_power_dbm = p
        self.antenna_dbi = a
        self.output_frequency_hz = f
    
