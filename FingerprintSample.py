from RSSISample import RSSISample
from math import *

class FingerprintSample:
    def __init__(self, samples: list[RSSISample]) -> None:
        self.samples = samples
    
    def addRSSI(self, rssiSamp: RSSISample):
        isIn = False
        sample : RSSISample
        for sample in self.samples:
            if sample.getMacAdd() == rssiSamp.getMacAdd():
                isIn = True
                break
   
        if isIn :
            #Ajouter à la liste rssi du rssiSample existant
            sample.addRSSI(rssiSamp.getRSSI())
        else:
            #Créer nvx rssiSample
            self.samples.append(rssiSamp)
    
    def calculateAvgRSSI(self)->None:
        for rssi in self.samples:
            rssi.calculateAvgRSSI()
        self.orderRSSI()

    def orderRSSI(self):
        self.samples.sort(key= lambda x : x.mac_address)