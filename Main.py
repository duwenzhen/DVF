import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import glob


path = r"."
from subprocess import check_output
print(check_output(["ls", path]).decode("utf8"))
all_files = glob.glob(path + "/valeursfoncieres*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0, sep='|')
    df = df.iloc[:, 7:].fillna(0)
    print(df.head())
    print(df.shape)
    li.append(df)
df = pd.concat(li, axis=0, ignore_index=True)
print(df.shape)
df = df.loc[df["Code type local"] == 2]
df["Surface Carrez du 1er lot"] = df["Surface Carrez du 1er lot"].str.replace(',','.').astype(float)
df["Surface Carrez du 2eme lot"] = df["Surface Carrez du 2eme lot"].str.replace(',','.').astype(float)
df["Surface Carrez du 3eme lot"] = df["Surface Carrez du 3eme lot"].str.replace(',','.').astype(float)
df["Surface Carrez du 4eme lot"] = df["Surface Carrez du 4eme lot"].str.replace(',','.').astype(float)
df["Surface Carrez du 5eme lot"] = df["Surface Carrez du 5eme lot"].str.replace(',','.').astype(float)
df["Valeur fonciere"] = df["Valeur fonciere"].str.replace(',', '.').astype(float)

df = df.fillna(0)
df = df.loc[(df["Surface Carrez du 1er lot"] != 0 )| (df["Surface Carrez du 2eme lot"] != 0)|(df["Surface Carrez du 3eme lot"] != 0)|(df["Surface Carrez du 4eme lot"] != 0)|(df["Surface Carrez du 5eme lot"] != 0)]
print(df["Code type local"].head())
print(df.shape)
df["ID"] = df["Code departement"].map(str) + df["Code commune"].map(str) + df["Prefixe de section"].map(str) + df["Section"].map(str) + df["No plan"].map(str) + df["No disposition"].map(str) + df["Type local"].map(str) + df["Date mutation"].map(str)
print(df.shape)
print(df["ID"].nunique())
df["SurfaceCarrez"] = df["Surface Carrez du 1er lot"].astype(float) + df["Surface Carrez du 2eme lot"].astype(float)+df["Surface Carrez du 3eme lot"].astype(float) +df["Surface Carrez du 4eme lot"].astype(float) +df["Surface Carrez du 5eme lot"].astype(float)

df = df.fillna(0)
df = df.loc[df["Valeur fonciere"] > 0]
df["PrixM2"] = df["Valeur fonciere"]  / df["SurfaceCarrez"]
df["Date mutation"] = pd.to_datetime(df["Date mutation"],format="%d/%m/%Y")
df.to_csv(r"./appartement.csv", sep='|')