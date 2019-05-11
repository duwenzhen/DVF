import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
color = sns.color_palette()

import glob


path = r""
df = pd.read_csv(path + "appartement.csv", index_col=0, header=0, sep=',')
df["Date mutation"] = pd.to_datetime(df["Date mutation"],format="%Y/%m/%d").astype(int)
df = df.drop(["No voie", "Type de voie", "Code voie", "Voie", "Commune", "Code commune", "Prefixe de section", "Section", "No plan", "No Volume", "1er lot", "2eme lot", "3eme lot", "4eme lot", "5eme lot", "ID"], axis=1)

#df["YearMonth"] = df["Date mutation"].dt.strftime('%Y%m')


dtype_df = df.dtypes.reset_index()
dtype_df.columns = ["Count", "Column Type"]
print(dtype_df)


print(df["PrixM2"].median())


tmp = df.groupby(["Code departement"])['PrixM2'].agg([np.median, np.mean, np.std])
#tmp = df[["Code departement",'PrixM2']]


#plt.figure(figsize=(24,12))
#sns.boxplot(x = tmp["Code departement"], y= df.groupby(["Code departement"])['PrixM2'])

#sns.barplot(tmp.index, tmp.values, alpha=0.8, color=color[3])
#sns.violinplot(
#    x='Code departement',
#    y='PrixM2',
#    data=tmp.groupby(["Code departement"])
#)
#plt.xticks(rotation='vertical')
#plt.xlabel('Price', fontsize=12)
#plt.ylabel('Date', fontsize=12)
#plt.show()

plt.figure(figsize=(12,6))
sns.barplot(tmp.index, tmp['std'], alpha=0.8, color=color[3])
#sns.barplot(tmp.index, tmp['mean'], alpha=0.8, color=color[3])
#sns.barplot(tmp.index, tmp['std'], alpha=0.8, color=color[3])
plt.xticks(rotation='vertical')
plt.xlabel('Price', fontsize=12)
plt.ylabel('Date', fontsize=12)
plt.show()
