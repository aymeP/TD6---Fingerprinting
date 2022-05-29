from math import log10

class RSSISample:
    """Classe representing an RSSISample. It contains:
        -its mac address : str
        -its list of rssi values : list[float]
    """

    def __init__(self, mac_address: str, rssi: list[float]) -> None:
        """Init the RSSISample"""
        self.mac_address = mac_address
        self.rssi = rssi
    
    def addRSSI(self, newRssi:list[float]) -> None:
        """Add a list of rssi values to the RSSISample
            :param newRssi: the list to add: list[float]
        """
        self.rssi += newRssi

    def get_average_rssi(self) -> list[float]:
        """Get the RSSISample's average rssi value.
            :return: a list[float] containing only the average
        """
        convert = 0
        #Convert the self.samples from dBm to mW
        for samp in self.rssi :
            convert += pow(10.0,samp/10.0)
        #Calculate the average
        moy = convert/len(self.rssi)
        #Convert the averag to dBm and return it
        return [round(10. * log10(moy),2)]
    
    def getMacAdd(self) -> str:
        """Get the RSSISample's mac_address.
            :return: str
        """
        return self.mac_address
    
    def getRSSI(self) -> list[float]:
        """Get the RSSISample's rssi value(s).
            :return: list[float]
        """
        return self.rssi
    
    def calculateAvgRSSI(self)->None:
        """Calculate the RSSISample's average rssi value"""
        self.rssi=self.get_average_rssi()