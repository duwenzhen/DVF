import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
import glob


path = r"."
from subprocess import check_output
print(check_output(["ls", path]).decode("utf8"))
all_files = glob.glob(path + "/valeursfoncieres*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0, sep='|')
    df = df.iloc[:, 7:]
    df = df.drop(["Type local", "Identifiant local", "B/T/Q"], axis = 1)
    print(df.head())
    print(df.shape)
    li.append(df)
df = pd.concat(li, axis=0, ignore_index=True)
print(df.shape)

CommuneDF = df['Commune'].unique()
np.savetxt("commune.csv", CommuneDF, delimiter=",", fmt="%s")

dtype_df = df.dtypes.reset_index()
dtype_df.columns = ["Count", "Column Type"]
dtype_df

leNC = preprocessing.LabelEncoder()
tmpdf = df['Nature culture'].fillna("0")
leNC.fit(tmpdf)


print(list(leNC.classes_))
df['Nature culture'] = leNC.transform(tmpdf)


leNCS = preprocessing.LabelEncoder()
tmpdf = df['Nature culture speciale'].fillna("0")
leNCS.fit(tmpdf)


print(list(leNCS.classes_))
df['Nature culture speciale'] = leNCS.transform(tmpdf)

df = df.loc[df["Code type local"] == 2]
df.loc["Adjudication" == df["Nature mutation"], "Nature mutation"] = 0
df.loc["Vente" == df["Nature mutation"], "Nature mutation"] = 3
df.loc["Echange" == df["Nature mutation"], "Nature mutation"] = 1
df.loc["Expropriation" == df["Nature mutation"], "Nature mutation"] = 2
df.loc["Vente en l'état futur d'achèvement" == df["Nature mutation"], "Nature mutation"] = 4
df.loc["Vente terrain à bâtir" == df["Nature mutation"], "Nature mutation"] = 5

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
df["ID"] = df["Code departement"].map(str) + "_"+ df["Code commune"].map(str) + "_"+  df["Prefixe de section"].map(str) + "_"+  df["Section"].map(str) + "_"+  df["No plan"].map(str) + "_"+  df["No disposition"].map(str) + "_"+  df["Code type local"].map(str) + "_"+  df["Date mutation"].map(str)
print(df.shape)
print(df["ID"].nunique())
df["SurfaceCarrez"] = df["Surface Carrez du 1er lot"].astype(float) + df["Surface Carrez du 2eme lot"].astype(float)+df["Surface Carrez du 3eme lot"].astype(float) +df["Surface Carrez du 4eme lot"].astype(float) +df["Surface Carrez du 5eme lot"].astype(float)

df = df.fillna(0)
df = df.loc[df["Valeur fonciere"] > 0]
df["PrixM2"] = df["Valeur fonciere"]  / df["SurfaceCarrez"]
df["Date mutation"] = pd.to_datetime(df["Date mutation"],format="%d/%m/%Y")
df.to_csv(r"./appartement.csv", sep=',')

dtype_df = df.dtypes.reset_index()
dtype_df.columns = ["Count", "Column Type"]
print(dtype_df)