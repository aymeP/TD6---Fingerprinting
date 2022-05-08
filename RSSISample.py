from math import log10

class RSSISample:
    def __init__(self, mac_address: str, rssi: list[float]) -> None:
        self.mac_address = mac_address
        self.rssi = rssi
    
    def addRSSI(self, newRssi:list[float]) -> None:
        self.rssi = self.rssi + newRssi

    def get_average_rssi(self) -> list[float]:
        convert = 0
        #Convert les self.samples des dBm en mW
        for samp in self.rssi :
            convert += pow(10.0,samp/10.0)
        #Calculer la moyenne
        moy = convert/len(self.rssi)
        #Convertir la moyenne en dBm
        return [round(10. * log10(moy),2)]
    
    def getMacAdd(self) -> str:
        return self.mac_address
    
    def getRSSI(self) -> list[float]:
        return self.rssi
    
    def calculateAvgRSSI(self)->None:
        self.rssi=self.get_average_rssi()