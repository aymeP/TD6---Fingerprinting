from math import sqrt

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

      """
      #Formule trouvée sur internet pr du bleutooth
      #10 ^ ((Measured Power -RSSI)/(10 * N))
      
      measuredRSSI = -69.0
      APRSSI = -80.0
      N = 2

      #pow(10,(Pt + Gr + Gt + 20*log10(vLambda) - Pr -20*log10(4*pi))/(10*i))
      return pow(10,(measuredRSSI - APRSSI)/(10 * N))
      """

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


def probability(histo1: NormHisto, histo2: NormHisto) -> float:
      tempo = {}

      for key in histo1.histogram.keys():
            if key in histo2.histogram:
                  tempo.update({key : min(histo1.histogram[key], histo2.histogram[key])})
      
      proba = 0
      for value in tempo.values():
            proba += value
      return proba

def histogram_matching(db: FingerprintDatabase, sample: NormHisto) -> SimpleLocation:
      val = 0
      loc = SimpleLocation(0,0,0)
      for pt in db.db:
            newVal = probability(sample, pt.histogram)
            if newVal > val:
                  val = newVal
                  loc = pt.loc
      return loc 

"""End Histogram matching"""