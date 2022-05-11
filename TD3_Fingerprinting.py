from math import sqrt, floor, exp, pi
from statistics import mean, stdev

from FingerprintDatabase import FingerprintDatabase
from SimpleLocation import SimpleLocation

"""Simple matching"""
def rssi_distance(sample1: dict[str, float], sample2: dict[str, float]) -> float:
      """
      Calcul la distance rssi entre les 2 samples
      -sample1 : contient les valeurs mesurées
      -sample2 : contient les valeurs connues
      """
      #norme des distances entre chaque rssi de chaque app
      #d = sqrt(somme(pow(RSSIi1 - RSSIi2, 2))

      #Test de longueur ==> tous les AP ne sont pas detectés a certains endroits ==> pas bon
      if len(sample1) != len(sample2):
            return 1000
      
      d = 0
      for mac_address in sample1.keys():
            #certaines adresses mac peuvent etre dans le dictionnaire sample1 mais pas dans sample2
            if (mac_address in sample2) :
                  d += pow(sample1[mac_address] - sample2[mac_address], 2)
            else :
                  return 1000
            
            #d += pow(sample1[mac_address] - sample2[mac_address], 2)
      return sqrt(d) 


def simple_matching(db: FingerprintDatabase, sample: dict[str, float]) -> SimpleLocation:
      #Pr chaque pt dans bdd : calculer rssi_distance. retourner les coord ou la distance est la plus faible

      distanceMin = 1000
      position = SimpleLocation(0,0,0)
      for fp in db.db:
            #Pour chaque point
            #Construire le dict {addresse mac : rssi}
            dictRSSI = {}
            for rssiSamp in fp.sample.samples:
                  dictRSSI.update({rssiSamp.mac_address : rssiSamp.rssi[0]})

            #Calculer la distance rssi
            newDistanceMin = rssi_distance(sample,dictRSSI)
            
            #Comparer la nouvelle distance a la plus petite deja calculee
            if newDistanceMin < distanceMin :
                  distanceMin = newDistanceMin
                  position = fp.position

      return position
"""End simple matching"""




"""Histogram matching"""
#histo : int = dbm et float = normalisation
class NormHisto:
      def __init__(self, histo: dict[int, float]):
            self.histogram = histo


class PointHisto:
      def __init__(self, loc : SimpleLocation, histo: NormHisto):
            self.loc = loc
            self.histogram = histo


def probability(histo1: dict, histo2: dict) -> float:
      """Fonction calculant la probabilité que histo1 (l'histogramme des mesures) correspondent à histo2 (histogramme sauvé en base)"""
      tempo = {}
      tabResult = []
      #Pour chaque probabilité de chaque adresse mac de histo1, récupérer la plus petite valeur entre une probabilité de histo1 et la correspondante en base
      for key in histo1.keys():
            for keyHisto in histo1[key].keys():
                  if key in histo2.keys()and keyHisto in histo2[key].keys():
                        tabResult.append(min(histo1[key][keyHisto], histo2[key][keyHisto]))
      
      #Sommer les probabilités obtenues précédement pour déterminer la probabilité globale que la mesure corresponde aux données en base testées
      proba = 0
      for value in tabResult:
            proba += value
      return proba


def histogram_matching(db: FingerprintDatabase, sample: NormHisto) -> SimpleLocation:
      val = 0
      loc = SimpleLocation(0,0,0)
      for pt in db.db:
            newVal = probability(sample.histogram, pt.histogram)
            if newVal > val:
                  val = newVal
                  loc = pt.loc
      return loc 


def normaliserList(sampleTestList : list) -> NormHisto:
      #sort list
      sampleTempo = sortListByMacAddress(sampleTestList)

      sampleTest = NormHisto({})
      #Normaliser sampleTempo
      for key, sampleValues in sampleTempo.items():
            nb = len(sampleValues)
            tempo = {}
            #pour chaque mesure dBm d'une adresse mac de sampleTempo, compter le nombre de mesures identiques 
            for val in sampleValues :
                  if val in tempo:
                        tempo[val] += 1
                  else :
                        tempo.update({val : 1.0})

            #Convertire tempo en un histogramme pour avoir la probabilité de chaque mesure dBm à la place de leur nomber d'occurence
            for keyTempo in tempo.keys():
                  tempo[keyTempo] = tempo[keyTempo]/nb

            #Ajouter le dictionnaire tempo au dictionnaire final contenant pour chaque adresse mac (key) son histogramme (tempo)
            sampleTest.histogram.update({key : tempo})
      return sampleTest


def sortListByMacAddress(sampleTestList : list) -> dict:
      sampleTempo = {}
      #Grouper les données de sampleTestList par adresse mac dans sampleTempo
      for val in sampleTestList:
            if val[0] in sampleTempo:
                  #si l'adresse mac (val[0]) est dans sampleTempo, ajouter la mesure dBm (val[1]) à la liste des dBm de l'adresse mac
                  sampleTempo[val[0]].append(val[1])
            else:
                  #Sinon, ajouter l'adresse mac et sa mesure dBm à sampleTempo
                  sampleTempo.update({val[0] : [val[1]]})
      return sampleTempo

"""End Histogram matching"""




"""Gauss matching"""
class GaussModel:
      def __init__(self, avg: float, stddev: float):
            self.average_rssi = avg
            self.standard_deviation = stddev

class GaussPoint:
      def __init__(self, loc : SimpleLocation, histo: dict):
            self.loc = loc
            self.histogram = histo


def createHistoFromDict(testSample : dict) -> dict :
      histoToTest = {}
      for mac_address, modelGauss in testSample.items():
            #Calculer l'histogramme
            histo = computeHistoValues(modelGauss.average_rssi, modelGauss.standard_deviation, 10)
            histoToTest.update({mac_address : histo})
      return histoToTest


def lookForBestLocation(computedHistoDataBase : FingerprintDatabase, histoToTest : dict) -> SimpleLocation:
      val = 0
      loc = SimpleLocation(0,0,0)
      for pt in computedHistoDataBase.db:
            newVal = probability(histoToTest, pt.histogram)
            if newVal > val:
                  val = newVal
                  loc = pt.loc
      return loc 


def gauss_matching(dataBase : FingerprintDatabase, sampleTestList : list) -> SimpleLocation:
      #Initialisation de la base contenant les modèles de Gauss
      computedHistoDataBase = initialiserGaussDataBase(dataBase)

      #Créer les modeles de Gauss des mesures à tester
      testSample = creatGaussModels(sortListByMacAddress(sampleTestList))

      #Création et sauvegarde des histogrammes pour chaque AP à partir des avg et stdev à tester
      histoToTest = createHistoFromDict(testSample)

      #Retourner la meilleur position
      return lookForBestLocation(computedHistoDataBase, histoToTest)


"""
def histogram_from_gauss(sample: GaussModel) -> RSSISample:
	# Your code
	pass
"""


def computeHistoValues(average_rssi : float, standard_deviation : float, xMinMax : int) -> dict:
      """Function that compute histogram values for all integer values of RSSI from floor(rssi_avg)-10 to floor(rssi_avg)+10"""
      #Calculer l'histogramme
      histo = {}
      for x in range (floor(average_rssi)-xMinMax, floor(average_rssi)+xMinMax):
            stddev = standard_deviation
            if stddev != 0 :
                  histo.update({x : 1/(standard_deviation * sqrt(2*pi))*exp(-1/2*pow((x-average_rssi)/standard_deviation,2))})
            else :
                  histo.update({x : 1})
      
      #Coefficienter les probabilités de l'histogramme pour que leur somme soit égale à 1
      probaTotal = sum(histo.values())
      for key in histo.keys():
            histo[key] = histo[key] / probaTotal
      
      return histo


def initialiserGaussDataBase(dataBase : FingerprintDatabase) -> FingerprintDatabase:
      gaussDataBase = FingerprintDatabase()
      #Calculer avg et stddev des rssi samples pour chaque AP de chaque position
      for fp in dataBase.db:
            histosAPosition = {}
            for rssiSamp in fp.sample.samples:
                  #Créer le GaussModel pour l'AP rssiSamp.mac_address
                  histosAPosition.update({rssiSamp.mac_address : GaussModel(mean(rssiSamp.getRSSI()), stdev(rssiSamp.getRSSI()) if(len(rssiSamp.getRSSI())>1) else 0)})
            #Ajouter tous les GaussModel pour la position fp.position à la base gaussDataBase
            gaussDataBase.append(GaussPoint(fp.position,histosAPosition))


      #Computes histogram values for all integer values of RSSI from floor(rssi_avg)-10 to floor(rssi_avg)+10 and stores computed histograms.
      computedHistoDataBase = FingerprintDatabase()
      for gp in gaussDataBase.db:
            histosAPosition = {}
            for mac_address, modelGauss in gp.histogram.items():
                  #Calculer l'histogramme
                  histo = computeHistoValues(modelGauss.average_rssi, modelGauss.standard_deviation, 10)
                  histosAPosition.update({mac_address : histo})
            computedHistoDataBase.append(GaussPoint(gp.loc,histosAPosition))

      return computedHistoDataBase


def creatGaussModels(testSampleSorted) :
      testSample ={}
      for mac_address, rssi in testSampleSorted.items():
            #Créer le GaussModel pour l'AP d'adresse mac mac_address
            testSample.update({mac_address : GaussModel(mean(rssi), stdev(rssi) if(len(rssi)>1) else 0)})
      return testSample


"""End Gauss matching"""