import numpy as np # linear algebra
import googlemaps
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import json
import ast
import matplotlib.pyplot as plt
import seaborn as sns
from math import sin, cos, sqrt, atan2, asin, radians

MajorCities = {"PARIS" : (48.8566, 2.3522), "LYON": (45.7640, 4.8357)}

def RequestViaGoogleAPI():
    with open(r'./Credentials/Maps') as f:
        ApiKey = f.readline()

    gmaps = googlemaps.Client(key=ApiKey)


    geocode_result = gmaps.geocode('Ermont,France')
    print(geocode_result)

    def GoogleGeocoding(commune):
        return gmaps.geocode(commune)


    df = pd.read_csv('commune.csv', index_col=None, header=0, sep=',', names = ["Commune"])
    df['Requested'] = df['Commune'].astype(str).apply(lambda L: L + ",France")
    df['Results'] = df['Requested'].astype(str).apply(lambda L: GoogleGeocoding(L))
    print(df.shape)

    df.to_csv(r'./CommuneWithGeoCoding.csv', index=False)

def haversine(gps1, gps2):
    if (gps1[0] == None or gps1[1] == None):
        return 0
    R = 6373.0

    lat1 = gps1[0]
    lon1 = gps1[1]
    lat2 = gps2[0]
    lon2 = gps2[1]

    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)

    a = sin(dphi / 2) ** 2 + \
        cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    distance = 2 * R * atan2(sqrt(a), sqrt(1 - a))
    return distance

def extractGPS(x):
    convertedVal = ast.literal_eval(x)
    if (len(convertedVal) > 0):
        return convertedVal[0]['geometry']['location']['lat'], convertedVal[0]['geometry']['location']['lng']
    print("Noval", x)
    return None, None


def LoadAndExtractToDataframe(filename):
    df = pd.read_csv(filename, index_col=None, header=0, sep=',')
    df['ResultsGPS'] = df.Results.apply(extractGPS)
    df['ResultsLat'] = df.ResultsGPS.apply(lambda x: x[0])
    df['ResultsLng'] = df.ResultsGPS.apply(lambda x: x[1])
    print(df.shape)
    return df

def ComputeDistanceToMajorCity(df, city):
    cityGPS = MajorCities[city]
    df['distanceTo' + city] = df.ResultsGPS.apply(lambda x : haversine(x, cityGPS))
    print(df.shape)

if __name__ == "__main__":
    df = LoadAndExtractToDataframe(r'./CommuneWithGeoCoding.csv')
    ComputeDistanceToMajorCity(df,"PARIS")
    ComputeDistanceToMajorCity(df,"LYON")
    df.to_csv(r'./CommuneWithGeoCodingWithDistanceToMajorCities.csv', index=False)
    '''plt.figure(figsize=(12, 12))
    sns.jointplot(x=df.ResultsLat.values, y=df.ResultsLng.values, size=10)
    plt.ylabel('Longitude', fontsize=12)
    plt.xlabel('Latitude', fontsize=12)
    plt.show()
'''