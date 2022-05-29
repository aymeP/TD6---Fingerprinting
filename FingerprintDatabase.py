from SimpleLocation import SimpleLocation
from Fingerprint import Fingerprint
from RSSISample import RSSISample
from FingerprintSample import FingerprintSample
from csv import *

class FingerprintDatabase:
	"""Class representing a database"""
	def __init__(self) -> None:
		"""Init the class"""
		self.db = []
	
	def append(self, fp) -> None:
		"""Add an element at the end of the database.
			:param fp: the element to add
		"""
		self.db.append(fp)
		
	def constains(self, location:SimpleLocation) -> int:
		"""Check if an element exists in the database at this SimpleLocation.
			:param location: the location to test : SimpleLocation
			:return: the element's index in the database if it exists, -1 else
		"""
		dbIndex = 0
		for fp in self.db:
			if fp.exists(location):
				return dbIndex
			dbIndex+=1
		return -1
	
	def addRSSI(self, dbIndex: int, rssiSamp: RSSISample) -> None:
		"""Add an RSSISample to the corresponding element in the database.
			:param dbIndex: the index of the element where to add the rssiSample
			:param rssiSamp: the rssiSample to add  
		"""
		self.db[dbIndex].addRSSI(rssiSamp)

	def populate(self,path:str, calculateAvg = True, delim = ";")->None:
		"""Populate the database using values from a file.
			:param path: the path of the file to import
			:param calculateAvg: to calculate or not the rssis' average. Default value: True
			:param delim: the delimiter to use. Default value: ";"
		"""
		# Open the file
		with open(path, newline='') as csvfile:
			#Seperate each lines and divide them into a table using the given delimiter
			spamreader = reader(csvfile, delimiter=delim, quotechar='|')
			
			#For each file's line
			for row in spamreader:
				#If it contains at least 4 elements (x, y, z and orientation)        
				if len(row) > 4 :
					#Get the line's coordinates
					location = SimpleLocation(float(row[0]), float(row[1]), float(row[2]))
					#For each line's RSSISamples, made of row[i] (the mac address) and (row[i+1]) (the rssi value)
					for i in range(4,len(row),2): 
						#Test if the coordinates are already present in the database
						dbIndex = self.constains(location)
						
						if dbIndex != -1:
							#A Fingerprint with the tested coordinates exists in the database
							#Add to the FingerprintSample the RSSISample
							self.addRSSI(dbIndex,RSSISample(row[i], [float(row[i+1])]))
						else:
							#There is no Fingerprint with the tested coordinates, create a new Fingerprint
							self.append(Fingerprint(location,FingerprintSample([RSSISample(row[i], [float(row[i+1])])])))
		if calculateAvg :
			self.calculateAvgRSSI()

	def generateCSV(self,path:str)->None:
		"""
		Generate a csv file. Each Fingerprint data are organised as follow: 
		-Its x,y,z set of values is unique over the entire file
		-Its orientation value is 0
		-Its pairs of RSSI samples (defined by a MAC address and its associated RSSI) are ordered by MAC addresses (ascending order)
		:param path: the path of the file to fill
		"""

		#Open/Create the csv file to fill
		with open(path, 'w', newline='') as csvfile:
			spamwriter = writer(csvfile, delimiter=',', quotechar='|', quoting=QUOTE_MINIMAL)
			#For each element of the database
			for dbRow in self.db:
				rowToExport=[]
				
				#Add x,y,z set of values
				rowToExport.append(dbRow.position.x)
				rowToExport.append(dbRow.position.y)
				rowToExport.append(dbRow.position.z)
				
				#Add 0 as orientation value
				rowToExport.append(0)

				#Add MAC addresses and their associated RSSI
				for rowSample in dbRow.sample.samples:
					rowToExport.append(rowSample.mac_address)
					rowToExport += rowSample.rssi

				#Write dbRow in the csv file
				spamwriter.writerow(rowToExport)

	def calculateAvgRSSI(self)->None:
		"""Calculate the average RSSI"""
		for fp in self.db:
			fp.calculateAvgRSSI()