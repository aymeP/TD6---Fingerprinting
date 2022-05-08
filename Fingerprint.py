from SimpleLocation import SimpleLocation
from FingerprintSample import FingerprintSample
from RSSISample import RSSISample

class Fingerprint:
	def __init__(self, position: SimpleLocation, sample: FingerprintSample) -> None:
		self.position = position
		self.sample = sample
	
	def exists(self, loc:SimpleLocation)->None:
		return self.position == loc
	
	def addRSSI(self, rssiSamp: RSSISample)->None:
		self.sample.addRSSI(rssiSamp)
	
	def calculateAvgRSSI(self)->None:
		self.sample.calculateAvgRSSI()
	
	def getPosition(self) -> str:
		return self.position.x + "," + self.position.y + "," + self.position.z