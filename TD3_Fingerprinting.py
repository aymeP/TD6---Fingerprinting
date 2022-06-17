from math import sqrt, floor, exp, pi
from statistics import mean, stdev

from FingerprintDatabase import FingerprintDatabase
from SimpleLocation import SimpleLocation



"""Simple matching"""
def rssi_distance(sample1: dict[str, float], sample2: dict[str, float]) -> float:
      """
      Calculate the rssi distance between 2 samples.
      :param sample1: the first rssi samples to compare
      :param sample2: the second rssi samples to compare
      :return: the computed distance
      """
      #Test the lengths. If the number of detected APs in each sample is not the same then the distance can not be computed  
      if len(sample1) != len(sample2):
            return 1000
      
      d = 0
      #Compute the distance between each value for each AP
      for mac_address in sample1.keys():
            if (mac_address in sample2) :
                  #If an AP's mac_address is in sample2 then compute the distance between these 2 values.
                  d += pow(sample1[mac_address] - sample2[mac_address], 2)
            else :
                  #Else the distance can not be computed
                  return 1000
      return sqrt(d) 


def simple_matching(db: FingerprintDatabase, sample: dict[str, float]) -> SimpleLocation:
      """
      Look in the database for the SimpleLocation corresponding to the measured sample.
      :param db: the database containing the known rssi values.
      :param sample: the measured rssi values used to determine the location.
      :return: the SimpleLocation corresponding to the measured sample.
      """
      #For each location in the database, compute the rssi_distance with the sample. Return the location where the distance is the shortest
      distanceMin = 1000
      position = SimpleLocation(0,0,0)
      for fp in db.db:
            #Build a dict containing the AP's mac address and its rssi value
            dictRSSI = {}
            for rssiSamp in fp.sample.samples:
                  dictRSSI.update({rssiSamp.mac_address : rssiSamp.rssi[0]})

            #Compute the rssi distance
            newDistanceMin = rssi_distance(sample,dictRSSI)
            
            if newDistanceMin < distanceMin :
                  distanceMin = newDistanceMin
                  position = fp.position

      return position
"""End simple matching"""





"""Histogram matching"""
class NormHisto:
      """
      Class used to save an histogram.
      """
      def __init__(self, histo: dict[int, float]):
            self.histogram = histo

class PointHisto:
      """
      Class used to store an histogram at a location.
      """
      def __init__(self, loc : SimpleLocation, histo: NormHisto):
            self.loc = loc
            self.histogram = histo


def normaliserDataBase(dataBase : FingerprintDatabase) -> FingerprintDatabase:
      """
      Normalize a database. To normalize = to make the sum of all beans of each histogram equal to 1.
      :param dataBase: the database to normalized.
      :return: the normalized database.
      """
      normalizedDataBase = FingerprintDatabase() #Database containing NormHistos for each location

      #Normalize rssi samples of each location
      for fp in dataBase.db:
            #Init  the histogram
            histo = NormHisto({})

            dictHisto = {}
            #For each AP the the location fp.position
            for rssiSamp in fp.sample.samples:
                  #Count the total number of rssis
                  compte = 0

                  #Count the occurence number of each rssi 
                  for rssi in rssiSamp.rssi :
                        if int(rssi) in histo.histogram:
                              histo.histogram[int(rssi)] += 1
                        else:
                              histo.histogram.update({int(rssi) : 1.0})
                        compte += 1
            
                  #Normalize the rssis
                  for key in histo.histogram.keys():
                        histo.histogram[key] = histo.histogram[key]/compte
            
                  #Add the normalized histogram to the dict containing all the histograms for the location
                  dictHisto.update({rssiSamp.mac_address : histo.histogram})
            #Add the dict containing all the histograms for the location to the database
            normalizedDataBase.append(PointHisto(fp.position,dictHisto))
      #Return the normalized database
      return normalizedDataBase


def normaliserList(sampleTestList : list) -> NormHisto:
      """
      Transform a list of mac address ane their rssi values into an histogram
      :param sampleTestList: the list to normalize
      :return: the histogram build using the list
      """
      #Sort the rssi values of sampleTestList by mac_address
      sampleTempo = sortListByMacAddress(sampleTestList)

      sampleTest = NormHisto({})
      #Normalize sampleTempo
      for key, sampleValues in sampleTempo.items():
            nb = len(sampleValues)
            tempo = {}
            #Count the occurence number of each rssi
            for rssi in sampleValues :
                  if rssi in tempo:
                        tempo[rssi] += 1
                  else :
                        tempo.update({rssi : 1.0})

            #Normalize the rssis (build the histogram)
            for keyTempo in tempo.keys():
                  tempo[keyTempo] = tempo[keyTempo]/nb

            #Add the histogram to the final dict containing an histogram for each mac address
            sampleTest.histogram.update({key : tempo})
      #Return the dict containing an histogram for each mac address in the list given in parameter
      return sampleTest


def histogram_matching(dataBase: FingerprintDatabase, sampleTestList: list) -> SimpleLocation:
      """
      Compare the measured rssi values to the known ones in the database to determine the location.
      :param dataBase: the database containing the known rssi values
      :param sampleTestList: the list of the measured rssi values
      :return: the computed location where the measured have been taken  
      """
      #Normalize the database (calculate an histogram for each AP of each location)
      normalizedDataBase = normaliserDataBase(dataBase)

      #Normalize the measures to test (build an histogram for each AP)
      sampleTest = normaliserList(sampleTestList)

      #Determine and return the best location
      return lookForBestLocation(normalizedDataBase, sampleTest.histogram)

"""End Histogram matching"""





"""Gauss matching"""
class GaussModel:
      """
      Class containing the values (an avg and a stdev) used to build a Gauss curve.
      """
      def __init__(self, avg: float, stddev: float):
            self.average_rssi = avg
            self.standard_deviation = stddev

class GaussPoint:
      """
      Class contaning a location and all the histograms associated to it.
      """
      def __init__(self, loc : SimpleLocation, histo: dict):
            self.loc = loc
            self.histogram = histo


def createHistoFromDict(testSample : dict) -> dict :
      """
      Build an histogram from a dict containing mac adresses and their corresponding average and standrad deviation values
      :param testSample: the dict used to create histograms.
      :return: a dict contaning an histogral for each mac adress 
      """
      histoToTest = {}
      for mac_address, modelGauss in testSample.items():
            #Build the histogram
            histo = computeHistoValues(modelGauss.average_rssi, modelGauss.standard_deviation, 10)
            histoToTest.update({mac_address : histo})
      return histoToTest


def gauss_matching(dataBase : FingerprintDatabase, sampleTestList : list) -> SimpleLocation:
      """
      Compare the measured rssi values to the known ones in the database to determine the location.
      :param dataBase: the database containing the known rssi values
      :param sampleTestList: the list of the measured rssi values
      :return: the computed location where the measure have been taken

      """
      #Initialize the database containing the Gauss models
      computedHistoDataBase = initialiserGaussDataBase(dataBase)

      #Build the Gauss models from the measured values to test
      testSample = createGaussModel(sortListByMacAddress(sampleTestList))

      #Build and save histogram for each AP using the avg et stdev values to test
      histoToTest = createHistoFromDict(testSample)

      #Determine and return the best location 
      return lookForBestLocation(computedHistoDataBase, histoToTest)
  

def computeHistoValues(average_rssi : float, standard_deviation : float, xMinMax : int) -> dict:
      """
      Function that compute histogram values for all integer values of RSSI from floor(rssi_avg)-xMinMax to floor(rssi_avg)+xMinMax.
      :param average_rssi: the average rssi value.
      :param standard_deviation: the stdev value.
      :param xMinMax: the value used as limits to build the histogram.
      :return: a dict  conatining the values of the histogram.
      """
      #Compute the histogram
      histo = {}
      for x in range (floor(average_rssi)-xMinMax, floor(average_rssi)+xMinMax):
            stddev = standard_deviation
            if stddev != 0 :
                  histo.update({x : 1/(standard_deviation * sqrt(2*pi))*exp(-1/2*pow((x-average_rssi)/standard_deviation,2))})
            else :
                  histo.update({x : 1})
      
      #Divide the probabilities by a coefficient so their sum is equal to 1
      probaTotal = sum(histo.values())
      for key in histo.keys():
            histo[key] = histo[key] / probaTotal
      
      #Return the computed histogram
      return histo


def initialiserGaussDataBase(dataBase : FingerprintDatabase) -> FingerprintDatabase:
      """
      Build a database containing Gauss values from rssi values contained in a database.
      :param dataBase: the database containing the rssi values of each AP for each location.
      :return: the build database containing the Gauss values.
      """
      gaussDataBase = FingerprintDatabase()
      #Calculate the avg and stdev values from the rssi samples for each AP of each location
      for fp in dataBase.db:
            histosAPosition = {}
            for rssiSamp in fp.sample.samples:
                  #Build and save the Gauss model for the AP rssiSamp.mac_address
                  histosAPosition.update({rssiSamp.mac_address : GaussModel(mean(rssiSamp.getRSSI()), stdev(rssiSamp.getRSSI()) if(len(rssiSamp.getRSSI())>1) else 0)})
            #Add all the Gauss models for the location fp.position to the database gaussDataBase
            gaussDataBase.append(GaussPoint(fp.position,histosAPosition))


      #Computes histogram values for all integer values of RSSI from floor(rssi_avg)-10 to floor(rssi_avg)+10 and stores the computed histograms.
      computedHistoDataBase = FingerprintDatabase()
      for gp in gaussDataBase.db:
            histosAPosition = {}
            for mac_address, modelGauss in gp.histogram.items():
                  #Compute the histogram
                  histo = computeHistoValues(modelGauss.average_rssi, modelGauss.standard_deviation, 10)
                  histosAPosition.update({mac_address : histo})
            computedHistoDataBase.append(GaussPoint(gp.loc,histosAPosition))
      #Return the database containing the Gauss values.
      return computedHistoDataBase


def createGaussModel(testSampleSorted: dict) -> dict:
      """
      Create a Gauss model from a dict containing rssi values for each mac adress.
      :param testSampleSorted: the dict containing rssi values for each mac adress.
      :return: a dict containing for each AP the avg and stdev values used to build the Gauss model
      """
      testSample ={}
      for mac_address, rssi in testSampleSorted.items():
            #Build the Gauss model for the AP having the adress mac mac_address
            testSample.update({mac_address : GaussModel(mean(rssi), stdev(rssi) if(len(rssi)>1) else 0)})
      return testSample

"""End Gauss matching"""





"""Common functions used for different matching"""
def lookForBestLocation(computedHistoDataBase : FingerprintDatabase, histoToTest : dict) -> SimpleLocation:
      """
      Look in the database to dertemine the best location of the histogram to test.
      :param computedHistoDataBase: the database containing the known histograms
      :param histoToTest: the histogram to test
      :return: the determined location where the measured have been made
      """
      val = 0
      loc = SimpleLocation(0,0,0)
      for pt in computedHistoDataBase.db:
            #Calculate the probability of each histogram in the database compared to the measured one
            newVal = probability(histoToTest, pt.histogram)
            if newVal > val:
                  val = newVal
                  loc = pt.loc
      return loc 


def probability(histo1: dict, histo2: dict) -> float:
      """
      Calculate the probability of an histogram to corresponds to another one.
      :param histo1: the histogram build from the measured rssis.
      :param histo2: the histogram saved in a database.
      :return: the probability of histo1 to correspond to histo2.
      """

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



def sortListByMacAddress(sampleTestList : list) -> dict:
      """
      Sort by mac_address the rssi values contained in a list.
      :param sampleTestList: the list to sort.
      :return: a dict containing the mac addresses and their corresponding rssi values
      """
      sampleTempo = {}
      #Group the sampleTestList's data by mac address in sampleTempo
      for val in sampleTestList:
            if val[0] in sampleTempo:
                  #If the mac address (val[0]) is in sampleTempo, add the measured rssi value (val[1]) to its rssis list
                  sampleTempo[val[0]].append(val[1])
            else:
                  #Else add the mac address and its rssi value to sampleTempo
                  sampleTempo.update({val[0] : [val[1]]})
      #Return the sorted list
      return sampleTempo

"""End Used for different matching"""