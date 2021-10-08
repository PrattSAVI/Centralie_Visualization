
#%% GAS
import os
import pandas as pd

folder = r'C:\Users\csucuogl\Desktop\WORK\Centralia\DATA\gas'

files = [i for i in os.listdir(folder) if i.split('.')[1] == "xlsx"]

dfg = pd.DataFrame()
for _ in files:
    temp = pd.read_excel( os.path.join(folder,_) )
    temp.columns = 'Date	Bore Hole	CH4	2	H2S	CO	Comments'.split("\t")
    dfg = dfg.append( temp )

display( dfg.head() )

dfg = dfg[ dfg['CH4'] != 'ppm' ]
dfg = dfg.replace( 'NIA' , None )
dfg['Date'] = pd.to_datetime( dfg['Date'] )

#Convert to numeric
dfg['CO'] = dfg['CO'].replace( ">500","500")
dfg['CO'] = dfg['CO'].astype(float)
dfg['CH4'] = dfg['CH4'].astype(float)
dfg.loc[ dfg['CO']>1000 , 'CO'] = 500

dfg.head()

#%%


import seaborn as sns
import matplotlib.pyplot as plt

sns.scatterplot( data=dfg , x='Date',y='CH4')
plt.show()


#%%

dfg.to_csv( os.path.join(folder,"gas.csv"))

# %%


folder = r'C:\Users\csucuogl\Desktop\WORK\Centralia\DATA\temp'

files = [i for i in os.listdir(folder) if i.split('.')[1] == "xlsx"]
print( files )
dft = pd.DataFrame()
for _ in files:
    temp = pd.read_excel( os.path.join(folder,_) )
    temp.columns = 'Date	Bore Hole	DepthFeet	Temp	Comments'.split("\t")
    temp = temp[ temp['Date'] != 'Date']
    dft = dft.append( temp )


dft = dft.dropna( how='all' , axis = 0)
dft = dft[ ~pd.isna( dft['Bore Hole']) ]
#dft['Date'] = pd.to_datetime( dft['Date'] )

display( dft )

#%%
dft['Temp'] = dft['Temp'].replace( '-' , None )
dft = dft[~pd.isna(dft['Temp'])] 
dft['Temp'] = dft['Temp'].astype(float)
# %%
sns.lineplot( data=dft , x='Date',y='Temp')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()

# %%

dft.groupby( by='Bore Hole' ).size().sort_values()

# %%

dft[ dft['Bore Hole'] == "N-10"]
# %%

dft.to_csv(os.path.join(folder,"temp.csv"))

# %%
