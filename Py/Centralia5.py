import board
import neopixel
import time
from colour import Color
from numpy import interp
import pandas as pd

#Start MSIC
from pygame import mixer
music_path = '/home/pi/Music/FireSounds.mp3'
mixer.init()
mixer.music.load(music_path)
mixer.music.play()

#INPUTS
led_count = 3
ring_count = 4

pixelNumber = (led_count*60) + (ring_count*16)

pixels = neopixel.NeoPixel(board.D18,
                           pixelNumber,
                           brightness=1,
                           pixel_order=neopixel.GRB,
                           auto_write=False)

path = '/home/pi/Desktop/Data/PerLED.csv'
df = pd.read_csv( path )
df['nr_value'] = df['nr_value'] * 100

#Calculate Color
graA = list( Color("black").range_to(Color("orange"),51) )
graB = list( Color("orange").range_to(Color("yellow"),51) )
gradient1 = graA + graB
gradient2 = list( Color("black").range_to(Color("yellow"),101) )

steps = 20
#Give it a test before it begins
for i in range(len(gradient1)):
    color = gradient1[ i ]
    color = tuple( [(color.rgb[0]*255),(color.rgb[1]*255),(color.rgb[2]*255)] )
    pixels[i] = color
    pixels.show()

time.sleep(1)
pixels.fill( (0,0,0) )
pixels.show()

def makecount(pre,pro,steps):
    dif = pro-pre
    iter = dif/steps
    return [ pre+ (iter*i) for i in range( steps )]

#START THE LOOP
print("Here we go!")
df = df[['year','led_c','nr_value']]
looper = 1

while looper < 2:
    for t in df['year'].unique():

        if t != 2021:
            temp = df[ df['year'] == t ]['nr_value'].tolist()
            nemp = df[ df['year'] == t+1 ]['nr_value'].tolist()
            leds = df[ df['year'] == t ]['led_c']

            for s in range(steps):
                for r in leds:
                    if r < 120: grad = gradient1
                    else: grad = gradient2

                    pre = temp[ r-1 ]
                    pro = nemp[ r-1 ]

                    color = grad[ int(makecount(pre,pro,steps)[s]) ]
                    color = tuple( [(color.rgb[0]*255),(color.rgb[1]*255),(color.rgb[2]*255)] )

                    pixels[ r ] = color
                
                pixels.show()
        else:
            temp = df[ df['year'] == t ]['nr_value'].tolist()
            leds = df[ df['year'] == t ]['led_c']
            for r in leds:
                if r < 120: grad = gradient1
                else: grad = gradient2

                pre = temp[ r-1 ]
                color = grad[ int(pre) ]
                color = tuple( [(color.rgb[0]*255),(color.rgb[1]*255),(color.rgb[2]*255)] )
                pixels[ r ] = color

        if sum(temp) == 0:
            time.sleep(0.5)
            print (t , "pass")
        else:
            time.sleep(4/steps)
            print (t , "stay")




mixer.music.stop()

pixels.fill( (0,0,0) )
pixels.show()