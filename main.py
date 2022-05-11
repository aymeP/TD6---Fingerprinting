from FingerprintDatabase import FingerprintDatabase
from TD2_GNSS_like_systems import *
from TD3_Fingerprinting import *



#Init database
dataBase = FingerprintDatabase()



"""Gauss matching"""
"""
#Lire le csv 
dataBase.populate('test_data_not_filtered.csv',False)

#Initialisation des données à tester
sampleTestList = [
      ["00:13:ce:97:78:79", -74],
      ["00:13:ce:95:e1:6f", -55],
      ["00:13:ce:8f:78:d9", -58],
      ["00:13:ce:95:de:7e", -51],
      ["00:13:ce:95:de:7e", -55],
      ["00:13:ce:95:e1:6f", -54],
      ["00:13:ce:97:78:79", -74],
      ["00:13:ce:8f:78:d9", -58],
      ["00:13:ce:8f:78:d9", -58],
      ["00:13:ce:97:78:79", -75],
      ["00:13:ce:95:e1:6f", -54],
      ["00:13:ce:95:de:7e", -59],
      ["00:13:ce:95:e1:6f", -51],
      ["00:13:ce:95:de:7e", -61],
      ["00:13:ce:95:e1:6f", -52],
      ["00:13:ce:8f:78:d9", -64],
      ["00:13:ce:95:de:7e", -59],
      ["00:13:ce:8f:78:d9", -62],
      ["00:13:ce:95:e1:6f", -56],
      ["00:13:ce:95:de:7e", -61],
      ["00:13:ce:95:de:7e", -54],
      ["00:13:ce:95:e1:6f", -57],
      ["00:13:ce:95:e1:6f", -55],
      ["00:13:ce:8f:78:d9", -61],
      ["00:13:ce:97:78:79", -75],
      ["00:13:ce:95:de:7e", -53]
]

sampleTestList = [
      ["00:13:ce:8f:78:d9",-37],
      ["00:13:ce:97:78:79",-73],
      ["00:13:ce:95:e1:6f",-63],
      ["00:13:ce:97:78:79",-73],
      ["00:13:ce:95:e1:6f",-60],
      ["00:13:ce:95:de:7e",-70],
      ["00:13:ce:97:78:79",-74],
      ["00:13:ce:8f:78:d9",-37],
      ["00:13:ce:95:e1:6f",-58],
      ["00:13:ce:8f:77:43",-84],
      ["00:13:ce:8f:78:d9",-37],
      ["00:13:ce:95:de:7e",-70],
      ["00:13:ce:95:e1:6f",-57],
      ["00:13:ce:95:e1:6f",-57],
      ["00:13:ce:8f:78:d9",-37],
      ["00:13:ce:8f:77:43",-83],
      ["00:13:ce:95:de:7e",-70],
      ["00:13:ce:8f:78:d9",-36],
      ["00:13:ce:97:78:79",-73],
      ["00:13:ce:95:e1:6f",-56],
      ["00:13:ce:8f:77:43",-83]
]

#Recherche de la meilleur position 
result = gauss_matching(dataBase, sampleTestList)
print ("Meilleur position : " + str(result.x) + ", " + str(result.y) + ", " + str(result.z))
"""
"""End Gauss matching"""





"""Histogram matching"""

#Lire le csv 
dataBase.populate('test_data_not_filtered.csv', False)


#Initialisation des données à tester
sampleTestList = [
      ["00:13:ce:97:78:79", -74],
      ["00:13:ce:95:e1:6f", -55],
      ["00:13:ce:8f:78:d9", -58],
      ["00:13:ce:95:de:7e", -51],
      ["00:13:ce:95:de:7e", -55],
      ["00:13:ce:95:e1:6f", -54],
      ["00:13:ce:97:78:79", -74],
      ["00:13:ce:8f:78:d9", -58],
      ["00:13:ce:8f:78:d9", -58],
      ["00:13:ce:97:78:79", -75],
      ["00:13:ce:95:e1:6f", -54],
      ["00:13:ce:95:de:7e", -59],
      ["00:13:ce:95:e1:6f", -51],
      ["00:13:ce:95:de:7e", -61],
      ["00:13:ce:95:e1:6f", -52],
      ["00:13:ce:8f:78:d9", -64],
      ["00:13:ce:95:de:7e", -59],
      ["00:13:ce:8f:78:d9", -62],
      ["00:13:ce:95:e1:6f", -56],
      ["00:13:ce:95:de:7e", -61],
      ["00:13:ce:95:de:7e", -54],
      ["00:13:ce:95:e1:6f", -57],
      ["00:13:ce:95:e1:6f", -55],
      ["00:13:ce:8f:78:d9", -61],
      ["00:13:ce:97:78:79", -75],
      ["00:13:ce:95:de:7e", -53]
]

sampleTestList = [
      ["00:13:ce:8f:78:d9",-37],
      ["00:13:ce:97:78:79",-73],
      ["00:13:ce:95:e1:6f",-63],
      ["00:13:ce:97:78:79",-73],
      ["00:13:ce:95:e1:6f",-60],
      ["00:13:ce:95:de:7e",-70],
      ["00:13:ce:97:78:79",-74],
      ["00:13:ce:8f:78:d9",-37],
      ["00:13:ce:95:e1:6f",-58],
      ["00:13:ce:8f:77:43",-84],
      ["00:13:ce:8f:78:d9",-37],
      ["00:13:ce:95:de:7e",-70],
      ["00:13:ce:95:e1:6f",-57],
      ["00:13:ce:95:e1:6f",-57],
      ["00:13:ce:8f:78:d9",-37],
      ["00:13:ce:8f:77:43",-83],
      ["00:13:ce:95:de:7e",-70],
      ["00:13:ce:8f:78:d9",-36],
      ["00:13:ce:97:78:79",-73],
      ["00:13:ce:95:e1:6f",-56],
      ["00:13:ce:8f:77:43",-83]
]


#Calcul de la meilleur position
result = histogram_matching(dataBase, sampleTestList)
print ("Meilleur position : " + str(result.x) + ", " + str(result.y) + ", " + str(result.z))

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