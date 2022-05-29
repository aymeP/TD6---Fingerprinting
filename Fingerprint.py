from SimpleLocation import SimpleLocation
from FingerprintSample import FingerprintSample
from RSSISample import RSSISample

class Fingerprint:
	"""Class representing an RSSI Fingerprint. It contains:
		-its position : SimpleLocation
		-its sample : FingerprintSample
	"""
	def __init__(self, position: SimpleLocation, sample: FingerprintSample) -> None:
		"""Init a Fingerprint"""
		self.position = position
		self.sample = sample
	
	def exists(self, loc:SimpleLocation)->None:
		"""Return if a location is equal to the class' one.
			:param loc: the SimpleLocation to test
		"""
		return self.position == loc
	
	def addRSSI(self, rssiSamp: RSSISample)->None:
		"""Add an RSSISample to the Fingerprint's sample
			:param rssiSamp: the rssiSamp to add
		"""
		self.sample.addRSSI(rssiSamp)
	
	def calculateAvgRSSI(self)->None:
		"""Calculate the average RSSI"""
		self.sample.calculateAvgRSSI()