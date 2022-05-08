from random import gauss
from statistics import stdev
from FingerprintDatabase import FingerprintDatabase
from TD2_GNSS_like_systems import *
from TD3_Fingerprinting import *


class GaussModel:
      def __init__(self, avg: float, stddev: float):
            self.average_rssi = avg
            self.standard_deviation = stddev

class GaussPoint:
      def __init__(self, loc : SimpleLocation, histo: NormHisto):
            self.loc = loc
            self.histogram = histo



def histogram_from_gauss(sample: GaussModel) -> RSSISample:
	# Your code
	pass





#Init database
dataBase = FingerprintDatabase()
#Lire le csv 
dataBase.populate('test_data_not_filtered.csv',False)
print("End Populating")





"""Gauss matching"""

#TODO histogram_from_gauss()

"""
De ce que je comprends, la classe GaussModel est faite pour chaque point avec 
-la moyen de tous les rssi mesurés au point
-stddev des rssi mesurés au point
"""

gaussDataBase = FingerprintDatabase()
#Calculer avg et stddev des rssi samples pour chaque point
for fp in dataBase.db:
      gaussList = []
      for rssiSamp in fp.sample.samples:
            moy = rssiSamp.get_average_rssi()
            if len(rssiSamp.rssi) > 1 :
                  std_dev = stdev(rssiSamp.rssi)
            else :
                  std_dev = 0
            gaussList.append(GaussModel(moy,std_dev))

      gaussDataBase.append(GaussPoint(fp.position,gaussList))






sampleTest = GaussModel()
#Comparer ce GaussModel avec les valeurs dans la base ?? ==> refaire la base avec que 1 GaussModel pour chaque point ??

#Avoir un GaussModel pour chaque mac_addr de chaque pt ?




#result = histogram_matching(normalizedDataBase, sampleTest)
#print ("Meilleur position : " + str(result.x) + ", " + str(result.y) + ", " + str(result.z))
"""End Gauss matching"""










"""Histogram matching"""
"""
normalizedDataBase = FingerprintDatabase()
#==> DB de position et NormHisto
#Lire le csv 
dataBase.populate('test_data_not_filtered.csv', False)
print("End Populating")

#Normaliser les rssi samples pour chaque point
for fp in dataBase.db:
      #Ajouter le SimpleLocation
      histo = NormHisto({})

      #Compter chaque rssi
      compte = 0
      for rssiSamp in fp.sample.samples:
            #histo.histogram.update({rssiSamp.mac_address : rssiSamp.rssi[0]/somme})
            for rssi in rssiSamp.rssi :
                  if int(rssi) in histo.histogram:
                        histo.histogram[int(rssi)] += 1
                  else:
                        histo.histogram.update({int(rssi) : 1.0})
                  compte += 1
      
      #Normaliser les rssi
      for key in histo.histogram.keys():
            histo.histogram[key] = histo.histogram[key]/compte
      
      normalizedDataBase.append(Point(fp.position,histo))


sampleTest = NormHisto({  
      -74:0.07692307692307693,
      -75:0.07692307692307693,
      -55:0.11538461538461539,
      -54:0.11538461538461539,
      -51:0.07692307692307693,
      -52:0.038461538461538464,
      -56:0.038461538461538464,
      -57:0.038461538461538464,
      -58:0.11538461538461539,
      -64:0.038461538461538464,
      -62:0.038461538461538464,
      -61:0.11538461538461539,
      -59:0.07692307692307693,
      -53:0.038461538461538464,
})

result = histogram_matching(normalizedDataBase, sampleTest)
print ("Meilleur position : " + str(result.x) + ", " + str(result.y) + ", " + str(result.z))
"""
"""End Histogram matching"""





"""
sampleTest = {
      "00:13:ce:8f:78:d9" :-70.93,
      "00:13:ce:95:de:7e" : 43.86,
      "00:13:ce:95:e1:6f" : -51.95}
"""
"""
"00:13:ce:95:e1:6f": -61.0,
"00:13:ce:95:de:7e": -62.0,
"00:13:ce:97:78:79": -63.0,
"00:13:ce:8f:77:43": -64.0,
"00:13:ce:8f:78:d9": -65.0}
"""

"""
sampleTest = {
      "00:13:ce:8f:78:d9" : -68.13,
      "00:13:ce:95:de:7e" : -41.43,
      "00:13:ce:95:e1:6f" : -51.69,
      "00:13:ce:97:78:79" : -66.57
}
"""
"""
sampleTest = {
      "00:13:ce:8f:77:43" : -56.46,
      "00:13:ce:8f:78:d9" : -60.58,
      "00:13:ce:95:de:7e" : -69.29,
      "00:13:ce:95:e1:6f" : -79.51,
      "00:13:ce:97:78:79" : -78.88
}
#Lire le csv 
dataBase.populate('test_data_not_filtered.csv')
print("End Populating")

result = simple_matching(dataBase, sampleTest)
print(result)
print ("Meilleur position : " + str(result.x) + ", " + str(result.y) + ", " + str(result.z))
"""










""" TD2
AP = {"00:13:ce:95:e1:6f": AccessPoint("00:13:ce:95:e1:6f", 4.93, 25.81, 3.55, 2417000000, 5.0, 20.0),
      "00:13:ce:95:de:7e": AccessPoint("00:13:ce:95:de:7e", 4.83, 10.88, 3.78, 2417000000, 5.0, 20.0),
      "00:13:ce:97:78:79": AccessPoint("00:13:ce:97:78:79", 20.05, 28.31, 3.74, 2417000000, 5.0, 20.0),
      "00:13:ce:8f:77:43": AccessPoint("00:13:ce:8f:77:43", 4.13, 7.085, 0.80, 2417000000, 5.0, 20.0),
      "00:13:ce:8f:78:d9": AccessPoint("00:13:ce:8f:78:d9", 5.74, 30.35, 2.04, 2417000000, 5.0, 20.0)}



#lire le CSV
dataBase.populate('test_result.csv')
#Pour chaque localisation, on calcul le i de chaque AP puis on calcul un i moyen pour chaque AP
#Distance = distance entre pt où on fait la mesure et l'AP

#Déterminer la position du mobile
result = determinerPosition(dataBase, AP)
print ("Meilleur position : " + str(result.x) + ", " + str(result.y) + ", " + str(result.z))
"""




""" TD1
#lire le CSV
#dataBase.populate('test_data.csv')
print("End Populating")
#Generate CSV
#dataBase.generateCSV('test_result.csv')
print("End Generating CSV")
"""