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



grouped = df.groupby(["Code departement"])['PrixM2']
tmp = grouped.agg([np.median, np.mean, np.std])

#plt.figure(figsize=(12,6))
plt.subplot(3, 1, 3)
sns.barplot(tmp.index, tmp['std'], alpha=0.8, color=color[3])
plt.xticks(rotation='vertical')
plt.xlabel('departement', fontsize=12)
plt.ylabel('standard deviation', fontsize=12)

plt.subplot(3, 1, 1)
sns.barplot(tmp.index, tmp['mean'], alpha=0.8, color=color[3])
plt.xticks(rotation='vertical')
plt.xlabel('departement', fontsize=12)
plt.ylabel('Mean Price', fontsize=12)

plt.subplot(3, 1, 2)
sns.barplot(tmp.index, tmp['median'], alpha=0.8, color=color[3])
plt.xticks(rotation='vertical')
plt.xlabel('departement', fontsize=12)
plt.ylabel('Median Price', fontsize=12)


plt.show()




df = df[df['PrixM2'] < df['PrixM2'].quantile(0.999)]
df = df[df['PrixM2'] > df['PrixM2'].quantile(0.001)]


grouped = df.groupby(["Code departement"])['PrixM2']
tmp = grouped.agg([np.median, np.mean, np.std])

#plt.figure(figsize=(12,6))
plt.subplot(3, 1, 3)
sns.barplot(tmp.index, tmp['std'], alpha=0.8, color=color[3])
plt.xticks(rotation='vertical')
plt.xlabel('departement', fontsize=12)
plt.ylabel('standard deviation', fontsize=12)

plt.subplot(3, 1, 1)
sns.barplot(tmp.index, tmp['mean'], alpha=0.8, color=color[3])
plt.xticks(rotation='vertical')
plt.xlabel('departement', fontsize=12)
plt.ylabel('Mean Price', fontsize=12)

plt.subplot(3, 1, 2)
sns.barplot(tmp.index, tmp['median'], alpha=0.8, color=color[3])
plt.xticks(rotation='vertical')
plt.xlabel('departement', fontsize=12)
plt.ylabel('Median Price', fontsize=12)


plt.show()
