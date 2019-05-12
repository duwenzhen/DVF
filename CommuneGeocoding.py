import numpy as np # linear algebra
import googlemaps
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


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