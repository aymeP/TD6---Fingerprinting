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

    #Define the search area
    Xmin = min(ap_locations.values(), key = lambda x : x.x).x
    Xmax = max(ap_locations.values(), key = lambda x : x.x).x
    Ymin = min(ap_locations.values(), key = lambda x : x.y).y
    Ymax = max(ap_locations.values(), key = lambda x : x.y).y
    Zmin = min(ap_locations.values(), key = lambda x : x.z).z
    Zmax = max(ap_locations.values(), key = lambda x : x.z).z

    #Initialize bestLoc and bestDist used to save the best data found
    bestLoc = SimpleLocation(Xmin, Ymin, Zmin)
    bestDist = 0
    for macAddr in ap_locations.keys():
        loc = ap_locations[macAddr]
        bestDist += abs(sqrt(pow(0 - loc.x, 2)+pow(0 - loc.y, 2)+pow(0 - loc.z, 2))-distances[macAddr])
    
    #Construct the points to test in the search area
    listX = construire_liste(round(Xmin, 1),round(Xmax, 1), step)
    listY = construire_liste(round(Ymin, 1),round(Ymax, 1), step)
    listZ = construire_liste(round(Zmin, 1),round(Zmax, 1), step)
    #For each point in the search area
    for x in listX : 
        for y in listY :
            for z in listZ : 
                dist = 0
                #Calculate and sum the distances between the tested point and each accesspoint
                for macAddr in ap_locations.keys():
                    loc = ap_locations[macAddr]
                    dist += abs(sqrt(pow(x - loc.x, 2)+pow(y - loc.y, 2)+pow(z - loc.z, 2))-distances[macAddr])
                
                #If the distance calculated is shorter than the best one, replace the previous best data by the current data
                if dist < bestDist :
                    bestDist = dist
                    bestLoc = SimpleLocation(x,y,z)

    return bestLoc
      
    
def construire_liste(nbMin, nbMax, pas, arrondi = 1)->list[float]:
    """Build a list of floats
        :param nbMin: the minimal number of the list
        :param nbMax: the maximal number of the list
        :param pas: the step between each number of the list
        :param arrondi: the round of the float number
        :return: list[float]
    """
    liste = []
    valeur = nbMin
    while (valeur < nbMax):
        valeur += pas
        liste.append(round(valeur, arrondi))
    return liste


def calibration(dataBase : FingerprintDatabase, AP : AccessPoint) -> list:
    """Calibration of the FBCM index of the access point.
        :param dataBase: the database used to calibrate the index
        :param AP: a dict containing the accesspoints to calibrate and their data
        :return: a list of the accesspoint's mac address and the corresponding index
    """
    #For each accesspoint, calculate all the FBCM indexes for each accespoint at each measured point in the database
    calibTab = []
    for fgp in dataBase.db:
        for rssiSamp in fgp.sample.samples:
            #Calculate the distance between the point where the measure is made and the accesspoint
            dist = fgp.position.distance(AP[rssiSamp.mac_address].location)
            calibTab.append([rssiSamp.mac_address, compute_FBCM_index(dist, rssiSamp, AP[rssiSamp.mac_address])])


    tabCalib = [] #List grouping the mac adresses and their FBCM indexes
    #For each index previously calculated, group them by address mac
    for calibInfo in calibTab:
        found = False
        for i in range(len(tabCalib)):
            if tabCalib[i][0] == calibInfo[0]:
                #If the adresse mac is already in tabcalibre, add the index to its list of indexes
                tabCalib[i][1].append(calibInfo[1])
                found = True
                break
        
        if not found:        
            #If the adresse mac not already in tabcalibre, add the mac address and the index to the list
            tabCalib.append([calibInfo[0],[calibInfo[1]]])

    #For each AP, calculate the fbcm idexes' average
    for calibInfo in tabCalib:
        calibInfo[1] = mean(calibInfo[1])
    """End Calibration"""
    return tabCalib


def calculerDistance(dataBase : FingerprintDatabase, AP : AccessPoint, tabCalib : list) -> dict:
    """Calculate the distance with each AP
        :param database: the database used to calibrate the FCBM indexes
        :param AP: the APs used to calculate a distance
        :param tabCalib: the calibrated FBCM indexes
    """
    #For each AP in the database, group their rssi and calculate their average
    rssiAvg = FingerprintSample([])
    for dbValue in dataBase.db:
        for rssiSamp in dbValue.sample.samples:
            rssiAvg.addRSSI(rssiSamp)
    rssiAvg.calculateAvgRSSI()

    #For each AP, calculate their distance and save it in a dict[mac_add, dist]
    dictDist = {}
    for apInfos in AP:
        for calib in tabCalib:
            if calib[0] == apInfos:
                for rssiSamp in rssiAvg.samples : 
                    if rssiSamp.getMacAdd() == apInfos :
                        rssi_avg = rssiSamp.getRSSI()[0]
                        break
                fbcm_index = calib[1]
                dictDist.update({apInfos : estimate_distance(rssi_avg, fbcm_index, AP[apInfos])})
    """End calculate the distance with each AP"""
    return dictDist


def determinerPosition(dataBase : FingerprintDatabase, AP : AccessPoint) -> SimpleLocation :
    """Determine the mobile's position.
        :param database: the database used to calibrate the FCBM indexes
        :param AP: the APs to calibrate and used to dertermine the mobile's position
        :return: the mobile's position
    """
    #Calibrate the APs
    tabCalib = calibration(dataBase, AP)

    #Calculate the distances
    dictDist = calculerDistance(dataBase, AP, tabCalib)

    """Determining the mobile's position"""
    #Build a dict containing each AP's position
    dictApLoc = {}
    for apInfos in AP.values():
        dictApLoc.update({apInfos.mac_address : apInfos.location})

    return multilateration(dictDist, dictApLoc)
    """End determining of the mobile's position"""