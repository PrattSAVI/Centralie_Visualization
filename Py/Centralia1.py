import board
import neopixel
import time
import random
from colour import Color

pixelNumber = 80 
pixels = neopixel.NeoPixel(board.D18,
                           pixelNumber,
                           brightness=0.5,
                           pixel_order=neopixel.GRBW,
                           auto_write=False)

def shutall():
    pixels.fill((0,0,0))

def ColorHill(color1,pix_range,pix_pos):

    c2 = Color(color1)
    c1 = Color("black")

    gradient1 = list( c1.range_to(c2,int(pix_range/2)+1))
    gradient2 = list( c2.range_to(c1,int(pix_range/2)+1))

    gradient = gradient1 + gradient2

    start_pix = int(pix_pos - (pix_range/2))
    end_pix = int(pix_pos + (pix_range/2))

    if start_pix < 0: start_pix=0
    if end_pix > pixelNumber:end_pix=pixelNumber

    #print( start_pix, end_pix , len(gradient) )

    for i in range( start_pix , end_pix ):
        r = int( gradient[i-start_pix].rgb[0] * 255 )
        g = int( gradient[i-start_pix].rgb[1] * 255 )
        b = int( gradient[i-start_pix].rgb[2] * 255 )
        #print( i, "-" ,r,g,b )
        pixels[i] = tuple([r,g,b])
    
    out_dict = {
        "start_pix":start_pix,
        "end_pix":end_pix,
        "grad":gradient
    }
    pixels.show()
    return out_dict

def transitions_Pix(p1,r1,p2,r2,steps):

    prange = [ round(p1 + (((p2-p1)/steps)*i)) for i in range(steps) ]
    rrange = [ round(r1 + (((r2-r1)/steps)*i)) for i in range(steps) ]

    for i in range(steps):
        shutall()
        out1 = ColorHill('#ffba08', rrange[i] ,prange[i] )
        #print( prange[i] , rrange[i] )
        time.sleep(0.01)

shutall()

max_time = int(45)
start_time = time.time()



cols = []
i=0
while( (time.time() - start_time) < max_time ):
    time.sleep(0.15)

    if i > 0:
        cols.append([random.randint(0,pixelNumber-10),random.randint(5,15)])
        transitions_Pix(cols[i-1][0],cols[i-1][1],cols[i][0],cols[i][1],random.randint(40,100))
    else:
        cols.append([random.randint(0,pixelNumber-10),random.randint(5,15)])
        transitions_Pix(0,0,cols[i][0],cols[i][1],random.randint(20,100))
    i = i + 1 
    print(time.time() - start_time)
shutall()
pixels.show()

print("Finished")
