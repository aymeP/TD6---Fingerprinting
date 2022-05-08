from math import pi, log10, sqrt
from statistics import mean
from AccessPoint import AccessPoint
from FingerprintDatabase import FingerprintDatabase
from RSSISample import RSSISample
from SimpleLocation import SimpleLocation
from FingerprintSample import FingerprintSample

step = 0.5

def compute_FBCM_index(distance: float, rssi_values: RSSISample, ap: AccessPoint) -> float:
    """
    Function compute_FBCM_index computes a FBCM index based on the distance (between transmitter and receiver)
    and the AP parameters. We consider the mobile device's antenna gain is 2.1 dBi.
    :param distance: the distance between AP and device
    :param rssi_values: the RSSI values associated to the AP for current calibration point. Use their average value.
    :return: one value for the FBCM index
    """

    Pr = rssi_values.getRSSI()[0]
    Pt = ap.output_power_dbm
    Gt = ap.antenna_dbi
    Gr = 2.1
    vLambda = 299792458 / ap.output_frequency_hz

    return ((Pt + Gr + Gt + 20*log10(vLambda) - Pr -20*log10(4*pi))/(10*log10(distance)))


def estimate_distance(rssi_avg: float, fbcm_index: float, ap: AccessPoint) -> float:
    """
    Function estimate_distance estimates the distance between an access point and a test point based on
    the test point rssi sample.
    :param rssi: average RSSI value for test point
    :param fbcm_index: index to use
    :param ap: access points parameters used in FBCM
    :return: the distance (meters)
    """
    
    Pr = rssi_avg
    Pt = ap.output_power_dbm
    Gt = ap.antenna_dbi
    Gr = 2.1
    vLambda = 299792458 / ap.output_frequency_hz
    i = fbcm_index

    return pow(10,(Pt + Gr + Gt + 20*log10(vLambda) - Pr -20*log10(4*pi))/(10*i))


def multilateration(distances: dict[str, float], ap_locations: dict[str, SimpleLocation]) -> SimpleLocation:
    """
    Function multilateration computes a location based on its distances towards at least 3 access points
    :param distances: the distances associated to the related AP MAC addresses as a string
    :param ap_locations: the access points locations, indexed by AP MAC address as strings
    :return: a location
    """

    #Calculer l'espace de recherche
    Xmin = min(ap_locations.values(), key = lambda x : x.x).x
    Xmax = max(ap_locations.values(), key = lambda x : x.x).x
    Ymin = min(ap_locations.values(), key = lambda x : x.y).y
    Ymax = max(ap_locations.values(), key = lambda x : x.y).y
    Zmin = min(ap_locations.values(), key = lambda x : x.z).z
    Zmax = max(ap_locations.values(), key = lambda x : x.z).z

    #Initialiser bestLoc et bestDist
    bestLoc = SimpleLocation(Xmin, Ymin, Zmin)
    bestDist = 0
    for macAddr in ap_locations.keys():
        loc = ap_locations[macAddr]
        bestDist += abs(sqrt(pow(0 - loc.x, 2)+pow(0 - loc.y, 2)+pow(0 - loc.z, 2))-distances[macAddr])
    
    #Pour chaque pt de l'espace de recherche
    listX = construire_liste(round(Xmin, 1),round(Xmax, 1), step)
    listY = construire_liste(round(Ymin, 1),round(Ymax, 1), step)
    listZ = construire_liste(round(Zmin, 1),round(Zmax, 1), step)
    for x in listX : 
        for y in listY :
            for z in listZ : 
                dist = 0
                for macAddr in ap_locations.keys():
                    loc = ap_locations[macAddr]
                    dist += abs(sqrt(pow(x - loc.x, 2)+pow(y - loc.y, 2)+pow(z - loc.z, 2))-distances[macAddr])
                
                if dist < bestDist :
                    bestDist = dist
                    bestLoc = SimpleLocation(x,y,z)

    return bestLoc
      
    
def construire_liste(nbMin, nbMax, pas, arrondi = 1):
    liste = []
    valeur = nbMin
    while (valeur < nbMax):
        valeur += pas
        liste.append(round(valeur, arrondi))
    return liste


def calibration(dataBase : FingerprintDatabase, AP : AccessPoint) -> list:
    """Calibration"""
    #Pour chaque AP, calculer index FBCM
    calibTab = []
    for fgp in dataBase.db:
        #Mettre en forme fgp.position
        apTab=[]
        for rssiSamp in fgp.sample.samples:
            #Distance = distance entre pt où on fait la mesure et l'AP
            dist = fgp.position.distance(AP[rssiSamp.mac_address].location)
            calibTab.append([rssiSamp.mac_address, compute_FBCM_index(dist, rssiSamp, AP[rssiSamp.mac_address])])


    tabCalib = [] #Tableau contenant les adresses mac et leur moyenne de l'index fbcm
    #Pour chaque AP, ajouter les index fbcm
    for calibInfo in calibTab:
        found = False
        for i in range(len(tabCalib)):
            if tabCalib[i][0] == calibInfo[0]:
                #si adresse mac dans tabcalibre, ajouter le i au tableau de i
                tabCalib[i][1].append(calibInfo[1])
                found = True
                break
        
        if not found:        
            #Sinon, ajouter l'add et le i
            tabCalib.append([calibInfo[0],[calibInfo[1]]])

    #Pour chaque AP, calculer la moyenne des index fbcm
    for calibInfo in tabCalib:
        calibInfo[1] = mean(calibInfo[1])
    """Fin Calibration"""
    return tabCalib


def calculerDistance(dataBase : FingerprintDatabase, AP : AccessPoint, tabCalib : list) -> dict:
    """Calcul de la distance avec chaque AP"""
    #Pour chaque AP dans dataBase, calculer la moyenne de ses rssi
    rssiAvg = FingerprintSample([])
    for dbValue in dataBase.db:
        for rssiSamp in dbValue.sample.samples:
            rssiAvg.addRSSI(rssiSamp)
    rssiAvg.calculateAvgRSSI()

    #Pour chaque AP, estimer la distance ==> les sauvegarder dans dict[mac_add, dist]
    dictDist = {}
    for apInfos in AP: #apInfos = l'adresse mac de l'ap
        for calib in tabCalib:
            if calib[0] == apInfos:
                for rssiSamp in rssiAvg.samples : 
                    if rssiSamp.getMacAdd() == apInfos :
                        rssi_avg = rssiSamp.getRSSI()[0]
                        break
                fbcm_index = calib[1]
                dictDist.update({apInfos : estimate_distance(rssi_avg, fbcm_index, AP[apInfos])})
    """Fin calcul de la distance avec chaque AP"""
    return dictDist


def determinerPosition(dataBase : FingerprintDatabase, AP : AccessPoint) -> SimpleLocation :
    #Calibrer les APs
    tabCalib = calibration(dataBase, AP)

    #Calculer les distances
    dictDist = calculerDistance(dataBase, AP, tabCalib)

    """Détermination de la position du mobile"""
    #Construction du dictionnaire contenant la position de chaque AP
    dictApLoc = {}
    for apInfos in AP.values():
        dictApLoc.update({apInfos.mac_address : apInfos.location})

    return multilateration(dictDist, dictApLoc)
    """Fin détermination de la position du mobile"""