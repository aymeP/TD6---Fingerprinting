from SimpleLocation import SimpleLocation

class AccessPoint:
    """Class representing an accespoint (AP). It contains:
        -its mac address: str
        -its location: SimpleLocation
        -output_power_dbm: float
        -antenna_dbi: float
        -output_frequency_hz: float
    """
    def __init__(self, mac: str, x:float, y:float, z:float, f=2417000000, a=5.0, p=20.0) -> None:
        """Init the class AccessPoint"""
        self.mac_address = mac
        self.location = SimpleLocation(x,y,z)
        self.output_power_dbm = p
        self.antenna_dbi = a
        self.output_frequency_hz = f
    
