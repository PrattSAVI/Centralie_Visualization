#%%
from numpy.lib.function_base import disp
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from colour import Color

import seaborn as sns
import matplotlib.pyplot as plt
from scipy.ndimage.filters import uniform_filter1d
import numpy as np

path = r"C:\Users\csucuogl\Documents\GitHub\Centralie_Visualization\Data\Gas Data Collected_V2.xlsx"

#CO2, CH4 - Upper
#CO,Particulates - Lower
#Temp - Circles
#Records - Perimter
leds = (60*6) + (16*4)

df = pd.read_excel( path , na_values='nan')
print( df.columns )


#These columns need to match with the data
cols = 'CO2 CH4 CO Temperature Particulates'.split( " " )

display( df )

#Convert text values to int.
for c in cols:
    print( c )

    #df[c] = df[c].astype(str)
    df[c] = df[c].str.strip()
    #df[c] = df[c].str.replace( 'nan' , None)
    df.loc[ df[c] == "Low Intensity" , c ] = 1
    df.loc[ df[c] == "Medium Intensity" , c ] = 2
    df.loc[ df[c] == "Medium Intensuity" , c ] = 2
    df.loc[ df[c] == "High Intensity" , c ] = 3

df

#%% Translate Data to LED blocks

import numpy as np
dn = df.copy()
dn = dn.fillna( 0 )
dn['around'] = np.where( dn['Records'] == "Y" , 1.0 , 0 )

dn['upper'] = dn['CO2'].astype(float) + dn['CH4'].astype(float)
dn['upper'] = dn['upper'].astype(float)
dn['lower'] = dn['CO'].astype(float) + dn['Particulates'].astype(float)
dn['lower'] = dn['lower'].astype(float)
dn['around'] = dn['around'].astype(float)
dn['rings'] = dn['Temperature'].astype(float)


dn['0-10'] = np.where( (dn['lower'] == 1) | (dn['lower'] == 2)  , dn['lower'] , 0  )
dn['10-20'] = np.where( (dn['lower'] == 3) | (dn['lower'] == 4)  , dn['lower'] , 0  )
dn['20-30'] = np.where( (dn['lower'] == 5) | (dn['lower'] == 6)  , dn['lower'] , 0  )

dn['30-40'] = np.where( (dn['upper'] == 1) | (dn['upper'] == 2)  , dn['upper'] , 0  )
dn['40-50'] = np.where( (dn['upper'] == 3) | (dn['upper'] == 4)  , dn['upper'] , 0  )
dn['50-60'] = np.where( (dn['upper'] == 5) | (dn['upper'] == 6)  , dn['upper'] , 0  )



#Scale to 0 and 1
def scale(A):
    return (A-np.min(A))/(np.max(A) - np.min(A))

cols = ['0-10','10-20','20-30','30-40','40-50','50-60']
for c in cols:
    dn[c] = scale( dn[c] ) 
dn = dn.fillna( 0 )
dn

#%%
dn = dn[dn['Year']>1960]
a = []

for i,r in dn.iterrows():
    for i in range(10): #10 steps for rows with values
        year_t = r['Year'] + (0.1 *i)
        a.append( [year_t] + r.tolist() )

p = ['year_t']
[p.append(i) for i in dn.columns.tolist()] 

df2 = pd.DataFrame( data = a , columns = p)
df2 = df2[ ['year_t','0-10','10-20','20-30','30-40','40-50','50-60','around','rings'] ]
df2.head(12)

#%%
dn = dn[dn['Year']>1960]
df2 = dn[['Year','0-10','10-20','20-30','30-40','40-50','50-60','around','rings']].copy()
cols = ['0-10','10-20','20-30','30-40','40-50','50-60','around','rings']

for c in cols:

    t = df2[c]
    t = uniform_filter1d( t, size=10 , mode='nearest')
    t = uniform_filter1d( t, size=5 , mode='nearest')
    t = scale(t)

    sns.lineplot( x=df2['Year'],y=df2[c] , color = 'grey' , alpha=0.5 )
    sns.lineplot( x=df2['Year'] , y=t )
    plt.show()

    df2[c + "_a"] = t


#%% Empty df to fill in, year - led number

a= []
for y in df2['Year'].unique():
    for _ in range(leds):
        a.append( [y,_] )

dl = pd.DataFrame( columns=["year","led_c"],data=a )
dl = dl.dropna( subset=['year'], axis = 0)
dl['x'] = None

#Assign X values to display on plot
dl.loc[ (dl['led_c']>=0) & (dl['led_c']<=60) , 'x' ] = "1_V.St"
dl.loc[ (dl['led_c']>60) & (dl['led_c']<=120) , 'x' ] = "2_V.St"
dl.loc[ (dl['led_c']>=120) & (dl['led_c']<=180) , 'x' ] = "3_V.St"
dl.loc[ (dl['led_c']>180) & (dl['led_c']<=240) , 'x' ] = "4_V.St"

dl.loc[ (dl['led_c']>240) & (dl['led_c']<=300) , 'x' ] = "4_C.St"
dl.loc[ (dl['led_c']>300) & (dl['led_c']<=360) , 'x' ] = "5_C.St"

dl.loc[ (dl['led_c']>360) , 'x' ] = "6_Rings"

dl['value'] = 0

dl

#%% Assign tenth values to all 4 strips
dn = df2.copy()
for i,r in dn.iterrows(): #Iterate Years in the wide data

    cols = ['0-10_a','10-20_a','20-30_a','30-40_a','40-50_a','50-60_a']
    for i in range(len(cols)):
        val = r[ cols[i] ]
        dl.loc[ (dl['year']==r['Year']) &  (dl['led_c'] >= 0 + (i*10) ) & (dl['led_c'] < 10 + (i*10) ) , 'value' ] = val
        dl.loc[ (dl['year']==r['Year']) &  (dl['led_c'] >= 110 - (i*10) ) & (dl['led_c'] < 120 - (i*10) ) , 'value' ] = val
        dl.loc[ (dl['year']==r['Year']) &  (dl['led_c'] >= 120 + (i*10) ) & (dl['led_c'] < 130 + (i*10) ) , 'value' ] = val
        dl.loc[ (dl['year']==r['Year']) &  (dl['led_c'] >= 230 - (i*10) ) & (dl['led_c'] < 240 - (i*10) ) , 'value' ] = val
 
    #Circular Strip
    dl.loc[(dl['year']==r['Year']) &  (dl['led_c'] >= 240 ) & (dl['led_c'] < 360 ) , 'value'] = r['around_a']

    #Rings
    dl.loc[(dl['year']==r['Year']) &  (dl['led_c'] >= 360 ) , 'value'] = r['rings_a']/3

dl[ dl['value'] > 0 ]
dl = dl.round(3)

dl 


#%%

dl3 = pd.DataFrame()
for i in dl['led_c'].unique(): 
    s = dl[ dl['led_c']== i].copy()
    noise = np.random.normal(0,2, len(s) ) 
    noise = np.where( s['value']>0 , noise , 0 )

    t = s['value'] + (noise*2) 
    t = np.where( t <=0 , 0 , t )

    t = uniform_filter1d( t, size=30 , mode='nearest')
    t = np.round( t , 2)
    
    s['value'] = t
    dl3 = dl3.append( s )

dl4 = pd.DataFrame()
for i in dl['x'].unique():
    s = dl[ dl['x']== i].copy()
    t = s['value']
    t = np.interp( t , (t.min(),t.max()) , (0,1))
    s['value'] = t
    dl4 = dl4.append( s )

dl4

# %% Plot
dl2 = dl4
import plotly.express as px
fig = px.scatter(dl2, x="x", y="led_c", animation_frame="year", animation_group="led_c", color="value" , range_x=[-1,4],
    color_continuous_scale=[(0, "black") ,(0.5, "orange"), (1, "yellow")] ,range_color=[0,dl2['value'].max()] )
fig.update_traces(marker_size=3)
fig.write_html(r"C:\Users\csucuogl\Desktop\WORK\Centralia\Chart\leds3.html")

#%%
dl2['nr_value'] = dl2['value']
dl2.to_csv( r"C:\Users\csucuogl\Documents\GitHub\Centralie_Visualization\Data\PerLED_2.csv" )
#%%
