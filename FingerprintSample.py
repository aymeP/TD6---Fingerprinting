from RSSISample import RSSISample
from math import *

class FingerprintSample:
    """Class representing a FingerprintSample. 
        It contains a list of RSSISamples
    """
    def __init__(self, samples: list[RSSISample]) -> None:
        """Init a FingerprintSample"""
        self.samples = samples
    
    def addRSSI(self, rssiSamp: RSSISample):
        """Add an RSSISample.
            :param rssiSamp: the RSSISample to add
        """
        isIn = False
        sample : RSSISample
        #Check if a sample has the same mac address as the given RSSISample
        for sample in self.samples:
            if sample.getMacAdd() == rssiSamp.getMacAdd():
                isIn = True
                break
        
        #If a sample has the same mac address as the given RSSISample, add the rssiSamp's rssi values to the existing sample
        if isIn :
            #Add the rssi values to an existing rssiSample
            sample.addRSSI(rssiSamp.getRSSI())
        else:
            #Add rssiSamp as a new rssiSample in the FingerprintSample
            self.samples.append(rssiSamp)
    
    def calculateAvgRSSI(self)->None:
        """Calculate the average rssi value of each RSSISample""" 
        for rssi in self.samples:
            rssi.calculateAvgRSSI()
        self.orderRSSI()

    def orderRSSI(self):
        """Order the rssi by mac_address"""
        self.samples.sort(key= lambda x : x.mac_address)