from SimpleLocation import SimpleLocation
from Fingerprint import Fingerprint
from RSSISample import RSSISample
from FingerprintSample import FingerprintSample
from csv import *

class FingerprintDatabase:
	def __init__(self) -> None:
		self.db = []
	
	def append(self, fp) -> None:
		self.db.append(fp)
		
	def constains(self, location:SimpleLocation) -> int:
		dbIndex = 0
		for fp in self.db:
			if fp.exists(location):
				return dbIndex
			dbIndex+=1
		return -1
	
	def addRSSI(self, dbIndex: int, rssiSamp: RSSISample) -> None:
		self.db[dbIndex].addRSSI(rssiSamp)

	def populate(self,path:str, calculateAvg = True)->None:
		with open(path, newline='') as csvfile:
			spamreader = reader(csvfile, delimiter=';', quotechar='|')
			
			for row in spamreader:        
				if len(row) > 4 :
					for i in range(4,len(row),2):
						#Récupération des coordonnéess et test de s'ils sont déja dans la base de données ou non
						location = SimpleLocation(float(row[0]), float(row[1]), float(row[2]))
						dbIndex = self.constains(location)
						
						if dbIndex != -1:
							#Il existe un Fingerprint avec les coordonnées testés
							#Ajouter au FingerprintSample du RSSISample
							self.addRSSI(dbIndex,RSSISample(row[i], [float(row[i+1])]))
						else:
							#Il n'existe pas Fingerprint avec les coordonnées testés
							#Création d'un Fingerprint avec les coordonnées testés
							self.append(Fingerprint(location,FingerprintSample([RSSISample(row[i], [float(row[i+1])])])))
		if calculateAvg :
			self.calculateAvgRSSI()

	def generateCSV(self,path:str)->None:
		"""
		Generer le csv et l'organiser de la manière suivante
		Its x,y,z set of values is unique over the entire file
		Its orientation value is 0
		Its pairs of RSSI samples (defined by a MAC address and its associated RSSI) are ordered by MAC addresses (ascending order)
		"""
		with open(path, 'w', newline='') as csvfile:
			spamwriter = writer(csvfile, delimiter=',', quotechar='|', quoting=QUOTE_MINIMAL)
			for dbRow in self.db:
				rowToExport=[]
				"""
				dbRow:
				-SimpleLocation
				-FingerprintSample ==> list RSSISample ==> mac_address + list rssi
				"""
				#Add x,y,z set of values
				rowToExport.append(str(dbRow.position.x))
				rowToExport.append(dbRow.position.y)
				rowToExport.append(str(dbRow.position.z))
				
				#Add 0 as orientation value
				rowToExport.append(0)

				#Add MAC addresses and their associated RSSI
				for rowSample in dbRow.sample.samples:
					rowToExport.append(rowSample.mac_address)
					rowToExport += rowSample.rssi

				#Write dbRow in the csv file
				spamwriter.writerow(rowToExport)

	def calculateAvgRSSI(self)->None:
		for fp in self.db:
			fp.calculateAvgRSSI()