#%% Import 
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

pixelNum = 80 #Change

def scaleColumn(s):
    return (s-s.min()) * pixelNum /(s.max()-s.min())

pd.set_option('display.max_columns', None)

path = r"C:\Users\csucuogl\Desktop\WORK\Centralia\DATA\airBeams\20211007.csv"
#path = r"C:\Users\csucuogl\Desktop\WORK\Centralia\DATA\airBeams\20210427.csv"
df = pd.read_csv( path )

#Simplify
df = df.drop( 'mac_address	firmware_ver	hardware'.split("\t") , axis=1 )
df = df.drop( ['rssi','uptime','gas','adc'] , axis = 1 )
df['UTCDateTime'] = pd.to_datetime( df['UTCDateTime'] )

df['p_10_0_um_b'] = df['p_10_0_um_b'].str.replace('\x1a','')
df['p_10_0_um_b'] = df['p_10_0_um_b'].astype(float)

df.head()

# %%  Graph Out
import random
graph = [
    'current_temp_f',
    'current_humidity',
    'pressure',
    'p_1_0_um',
    'p_2_5_um',
    'p_5_0_um',
    'p_10_0_um' ]

for _ in graph:
    col = "norm_" + _ #New Column Name
    df["norm_" + _] = scaleColumn( df[_] ) #Scale each columns
    plt.figure(figsize=(12,1)) 
    sns.lineplot(
        data = df,
        x = 'UTCDateTime' , y = col,
        color = "black",
        alpha = 0.7
    )
    plt.xticks( rotation = 90 )
    sns.despine( top=True,right=True)
    plt.title( col )
    plt.ylabel("")
    plt.show()

# %% Are they realted

df2 = df[ graph ]
sns.heatmap( df2.corr() , cmap='coolwarm')

# %% Only keep normalized columns

dfn = df[ ['UTCDateTime']  + df.columns[ df.columns.str.contains("norm_") ].tolist() ]
dfn.head()

# %%
