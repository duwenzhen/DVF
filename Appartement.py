import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
color = sns.color_palette()

import glob


path = r""
df = pd.read_csv(path + "appartement.csv", index_col=None, header=0, sep=',')
df["Date mutation"] = pd.to_datetime(df["Date mutation"],format="%Y/%m/%d")
df["YearMonth"] = df["Date mutation"].dt.strftime('%Y%m')


dtype_df = df.dtypes.reset_index()
dtype_df.columns = ["Count", "Column Type"]
print(dtype_df)




tmp = df.loc[df["Code departement"] == 75].groupby(['YearMonth'])['PrixM2'].count()


plt.figure(figsize=(8,6))
plt.scatter(range(df.shape[0]), np.sort(np.log(df.PrixM2.values)))
plt.xlabel('index', fontsize=12)
plt.ylabel('PrixM2', fontsize=12)
plt.show()

plt.figure(figsize=(12,6))
sns.barplot(tmp.index, tmp, alpha=0.8, color=color[3])
plt.xticks(rotation='vertical')
plt.xlabel('Price', fontsize=12)
plt.ylabel('Date', fontsize=12)
plt.show()


tmp = df.loc[df["Code postal"] == 75016].groupby(['YearMonth'])['PrixM2'].median()


plt.figure(figsize=(12,6))
sns.barplot(tmp.index, tmp, alpha=0.8, color=color[3])
plt.xticks(rotation='vertical')
plt.xlabel('Price', fontsize=12)
plt.ylabel('Date', fontsize=12)
plt.show()