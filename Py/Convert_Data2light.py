#%%
from numpy.lib.function_base import disp
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import time
from colour import Color
from seaborn.distributions import distplot

path = r"C:\Users\csucuogl\Downloads\Gas Data Collected_V2.xlsx"

#CO2, CH4 - Upper
#CO,Particulates - Lower
#Temp - Circles
#Records - Perimter
leds = (60*3) + (16*4)

df = pd.read_excel( path)

cols = 'CO2	CH4	CO	Particulates	Temperature'.split( "\t" )

for c in cols:

    df[c] = df[c].str.strip()

    df.loc[ df[c] == "Low Intensity" , c ] = 1
    df.loc[ df[c] == "Medium Intensity" , c ] = 2
    df.loc[ df[c] == "High Intensity" , c ] = 3

df.head(15)

#%% Empty df to fill in, year - led number

a= []
for y  in df['Year'].unique():
    for _ in range(leds):
        a.append( [y,_] )

dl = pd.DataFrame( columns=["year","led_c"],data=a )
dl['year'] = dl['year'].astype(int)
dl['x'] = None

#Assign X values to display on plot
dl.loc[ (dl['led_c']>=0) & (dl['led_c']<=60) , 'x' ] = "1_V.St"
dl.loc[ (dl['led_c']>60) & (dl['led_c']<=120) , 'x' ] = "2_V.St"
dl.loc[ (dl['led_c']>120) & (dl['led_c']<=180) , 'x' ] = "3_C.St"
dl.loc[ (dl['led_c']>180) , 'x' ] = "4_Rings"

dl['value'] = 0

#Assign LED values to High, Med, Low
def getLED_begin(v):
    return v*10

def getLED_second(v):
    return v*10+30

def getLED_Mirror_begin(v):
    if v == 1: return 120
    if v == 2: return 110
    if v == 3: return 100

def getLED_Mirror_second(v):
    if v == 1: return 90
    if v == 2: return 80
    if v == 3: return 70

for i,r in df.iterrows():

    #Upper 0-30
    col = 'CO2'
    if not pd.isna( r[col] ):
        dl.loc[ (dl['year'] == r['Year']) & (dl['led_c'] > getLED_begin(r[col])-10) & (dl['led_c']< getLED_begin(r[col]) ) , 'value'] = dl[(dl['year'] == r['Year']) & (dl['led_c']> getLED_begin(r[col])-10) & (dl['led_c'] < getLED_begin(r[col]) )]['value'] + 1
        dl.loc[ (dl['year'] == r['Year']) & (dl['led_c'] > getLED_Mirror_begin(r[col])-10) & (dl['led_c']< getLED_Mirror_begin(r[col]) ) , 'value'] = dl[(dl['year'] == r['Year']) & (dl['led_c']> getLED_Mirror_begin(r[col])-10) & (dl['led_c'] < getLED_Mirror_begin(r[col]) )]['value'] + 1

    col = 'CH4'
    if not pd.isna( r[col] ):
        dl.loc[ (dl['year'] == r['Year']) & (dl['led_c']> getLED_begin(r[col])-10) & (dl['led_c']< getLED_begin(r[col])) , 'value'] = dl[(dl['year'] == r['Year']) & (dl['led_c']> getLED_begin(r[col])-10) & (dl['led_c']< getLED_begin(r[col])*10)]['value'] + 1
        dl.loc[ (dl['year'] == r['Year']) & (dl['led_c']> getLED_Mirror_begin(r[col])-10) & (dl['led_c']< getLED_Mirror_begin(r[col])) , 'value'] = dl[(dl['year'] == r['Year']) & (dl['led_c']> getLED_Mirror_begin(r[col])-10) & (dl['led_c']< getLED_Mirror_begin(r[col])*10)]['value'] + 1

    #Lower 30-60
    col = 'CO'
    if not pd.isna( r[col] ):
        print( "CO->",r['Year'],r['CO'] , getLED_second(r[col]) )
        dl.loc[ (dl['year'] == r['Year']) & ( dl['led_c']> getLED_second(r[col])-10 ) & (dl['led_c']< getLED_second(r[col])) , 'value' ] = dl[(dl['year'] == r['Year']) & ( dl['led_c']> getLED_second(r[col])-10 ) & (dl['led_c']< getLED_second(r[col]))]['value'] + 1
        dl.loc[ (dl['year'] == r['Year']) & ( dl['led_c']> getLED_Mirror_second(r[col])-10 ) & (dl['led_c']< getLED_Mirror_second(r[col])) , 'value' ] = dl[(dl['year'] == r['Year']) & ( dl['led_c']> getLED_Mirror_second(r[col])-10 ) & (dl['led_c']< getLED_Mirror_second(r[col]))]['value'] + 1

    # ----- Add Particualtes ---- ? 

    #Circular Strip
    if r['Records'] == "Y":
         dl.loc[ (dl['year'] == r['Year']) & (dl['led_c']> 120 ) & (dl['led_c']<= 180 ) , 'value'] = 1

    #Rings
    col = 'Temperature'
    if not pd.isna( r[col] ):
        dl.loc[ (dl['year'] == r['Year']) & (dl['led_c']> 180 ) , 'value'] = r[col]*2/3

dl[ (dl['value']!=0) & (dl['led_c'] > 30) & (dl['led_c'] < 60) ].head()


#%% SMOOTHER CURVES
import seaborn as sns
from scipy.ndimage.filters import uniform_filter1d
import numpy as np

#PLot the whole dataset
ds = pd.DataFrame( columns = dl.columns )
sns.lineplot( data=dl, x='year',y='value')
plt.show()

#On Stripes move bloks of 10 by 10 and smoothen the curves using filter1d
for i in range(10,130,10):
    start,end = [i-10,i]
    temp = dl[ (dl['led_c']>start) & (dl['led_c']<=end) ].copy()
    temp['sm_value'] = 0 #blank for now

    if temp.sum()['value'] != 0: #If there is values assigned to these

        #Smoothened Value
        temp['sm_value'] = uniform_filter1d( temp['value'], size=45 , mode='nearest')

        #Add some noise to make think flicker
        temp['noise'] = np.random.normal(0,2, len(temp) )
        temp['noise'] = temp['sm_value'] * temp['noise']
        temp['noise'] = [np.interp( r , (temp['noise'].min(),temp['noise'].max()) , (0,1)  ) if r > 0 else 0 for i,r in temp['noise'].iteritems()  ]

        temp['sm_value'] = temp['sm_value'] + temp['noise']

        #PLOT
        [plt.axvline(x=t , color = '#555' , lw=0.25) for t in temp['year'].unique()]
        sns.lineplot( data = temp , x = 'year' , y='value', color='grey', alpha=0.5)
        sns.lineplot( x = temp['year'] , y = temp['sm_value'] , color = 'red' , alpha = 0.7 )
        plt.title('Pixels from {}-{}'.format(start,end))
        plt.show()

    ds = ds.append( temp )

#Increase Smoothened values to max (0,2)
ds['sm_value'] = [np.interp( r , (ds['sm_value'].min(),ds['sm_value'].max()) , (0,2)  ) for i,r in ds['sm_value'].iteritems()]

dl['sm_value'] = dl['value']
ds = ds.append( dl[ dl['led_c']>120] ) #Bring in Led 3 and Rings in
dl = dl.drop( "sm_value",axis=1)
ds.head(10)

# %% Plot

import plotly.express as px
fig = px.scatter(ds, x="x", y="led_c", animation_frame="year", animation_group="led_c", color="sm_value" , range_x=[-1,4],
    color_continuous_scale=[(0, "black") ,(0.5, "orange"), (1, "yellow")] ,range_color=[0,ds['sm_value'].max()] )
fig.update_traces(marker_size=3)
fig.write_html(r"C:\Users\csucuogl\Desktop\WORK\Centralia\Chart\leds.html")


# %% Smooth out everything on pixel by pixel basis!

val = uniform_filter1d( ds[ ds['led_c'] == 25 ]['sm_value'] , size=3 , mode='nearest')

[plt.axvline(x=t , color = '#555' , lw=0.25) for t in temp['year'].unique()]

sns.lineplot( 
    x = ds[ ds['led_c'] == 25 ]['year'] ,
    y= ds[ ds['led_c'] == 25 ]['sm_value'] , color = 'grey')

sns.lineplot( 
    x = ds[ ds['led_c'] == 25 ]['year'] ,
    y=val )

# %%

ds['nr_value'] = ds['sm_value']/2

#ds.to_csv(r"C:\Users\csucuogl\Desktop\WORK\Centralia\DATA\PerLED.csv")

ds['nr_value'] = ds['nr_value']*100
ds['nr_value'].hist( bins = 100)

# %%

ds = ds[['year','led_c','nr_value']]

def makecount(start,end,ranger):
    dif = start - end
    iter = dif / ranger
    return [start + (iter*i) for i in range(ranger)]

steps = 10

for t in ds['year'].unique():
    temp = ds[ ds['year'] == t]
    tnext = ds[ ds['year'] == t+1]

    for i,r in temp.iterrows():
        pre = ds.loc[ ( ds['year'] == t) & (ds['led_c'] == r['led_c']) , 'nr_value'].tolist()[0]
        pro = ds.loc[ ( ds['year'] == t+1) & (ds['led_c'] == r['led_c']) , 'nr_value'].tolist()[0]
        print( pre,pro)
        print( makecount(pre,pro,steps) )        


    if temp.sum()['nr_value'] != 0:
        display( temp.head() )
        display( tnext.head() )
        break

# %%


