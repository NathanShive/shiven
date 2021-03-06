# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 09:07:41 2014
@author: matthews
"""

import os, pygame, math
from pygame.locals import *
import random
import numpy as np

if __name__ == "__main__":
    main_dir = os.getcwd() 
else:
    main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

def handleInput(screen):
    #Handle Input Events
    for event in pygame.event.get():
        if event.type == QUIT:
            return True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return True
            elif event.key == K_s:
                pygame.event.set_blocked(KEYDOWN|KEYUP)
                fname = raw_input("File name?  ")
                pygame.event.set_blocked(0)
                pygame.image.save(screen,fname)
    return False



noiseTable = []                             #noise Table to hold random values between 0 and 1
hashTable = {}                              #hash table to hold a random permutaion of indicies into the noiseTable
for i in range(0,256,1):                    #populate noiseTable with random values between 0 and 1
    r = random.random()
    noiseTable.append(r)
    hashTable[i] = i

    
for i in range(0,256,1):                    #shuffle the hashTable so that it contains a random permutation
    r = random.randint(0,i)
    hashTable[i] = hashTable[r]
    hashTable[r] = i


def latticeNoise(x,y):
    return noiseTable[hashTable[(x+hashTable[y%255])%255]]


def smerp2(a,b):
    intx = math.floor(a)
    inty = math.floor(b)
    pctx = a - intx
    pcty = b - inty
    aa = latticeNoise(intx,inty)
    ab = latticeNoise(intx,inty+1)
    ba = latticeNoise(intx+1,inty)
    bb = latticeNoise(intx+1,inty+1)
    xa= smerp(pctx, aa, ba)
    xb= smerp(pctx, ab, bb)
    return smerp(pcty, xa, xb)


def smerp(pct,a,b):
    sq = pct**2
    qu = pct**3
    math1 = ((3)*sq)
    math2 = math1 - 2*qu
    #print("sq: %f"%sq)Marble
    #print("qu: %f"%qu)
    #print("math1: %f"%math1)
    #print("math2: %f"%math2)
    return a + math2*(b-a)


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Noise!')

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))#64,128,255
    #background.fill((0, 0, 0))#64,128,255
#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Prepare Game Objects
    clock = pygame.time.Clock()

    going = True
    pixelsize = 256 # power of 2
    width, height = screen.get_size()
    # main loop
    
    exp = 5                                            #This is the number of different frequncys I add up
    waveLength = 100                                    #This is my wavelength value
    frequency = 2                                       #frequency is 2^i
    persistence = 2.0                                   #I think this is a persitance value
    
    while going:
       
        while pixelsize > 0:
            print("psize : %i" % pixelsize)
            clock.tick(1)
            for x in range(0,width,pixelsize):
                xx = x/float(width)                     #normalized y cordinates
                lx = x/float(waveLength)                #latice y cordinates

                for y in range(0,height,pixelsize):
                    #clock.tick(2)
                    yy = y/float(height)                #normalized x cordinates
                    ly = y/float(waveLength)            #latice x cordinates
                    # draw into background surface                    
                    r = 0
                    for e in range(1,exp,1):            # I found I had to start this loop at 1 not 0, becuase if I start with 0 my values grow larger than 1
                        r = r + (smerp2(lx*(frequency**e),ly*(frequency**e))/persistence**e)
                    #r = smerp2(lx,ly)
                    #I wasnt sure how to best show the images I have created so I have simply commented out all of my differnt images
                    #=============THE COLORS BELOW GIVE ME SMOKEY CLOUDY PICTURES WITH DIFFERENT COLORS==================================
                    color = (255)*np.array((r,r,1))         #gives me blue and white sky
                    #color = (255)*np.array((1-r,r,1))       #blue and perple sky
                    #color = (255)*np.array((r,r,r))         #smoke
                    #color = (255)*np.array((1,r,r))         #red smoke
                    #color = (255)*np.array((1,r,1-r))       #pink and yellow
                    #color = (255)*np.array((r,r,0))         #yellow and black
                    #color = (255)*np.array((1-r,1-r,0))     #Black and yellow
                    #color = (255)*np.array((1-r,1-r/2,0))   #green yellow cloud
                    #color = (255)*np.array((1-r/2,1-r,0))   #Fire
                    #color = (140+(60*(r)),70+(25*r),20)     #Dirt
                    #color = (255)*np.array((r,r,r))         #Grey
                    #============HERE I WAS PLAYING WITH MULLTIPLE COLORS================================================================
                    '''blue and perple sky
                    if r < (1/3.0):
                        r = 3*r
                        color = (255)*np.array((0,r,1))         #gives me blue 
                    elif r < (2/3.0):
                        r = 3*r-1
                        color = (255)*np.array((r,1,1-r))         #gives me green
                    else:
                        r = 3*r-2
                        color = (255)*np.array((1,1-r,0))         #gives me red
                    '''
                    #===========THE COLORS BELLOW GIVE ME A 10LEVEL TOPIGRAPHICAL MAP====================================================
                    '''
                    if r < (1/10.0):
                        color = (0,0,255)
                    elif r < (2/10.0):
                        color = (0,128,255)
                    elif r < (3/10.0):
                        color = (0,255,255)
                    elif r < (4/10.0):
                        color = (0,255,128)
                    elif r < (5/10.0):
                        color = (0,255,0)
                    elif r < (6/10.0):
                        color = (128,255,0)
                    elif r < (7/10.0):
                        color = (255,255,0)
                    elif r < (8/10.0):
                        color = (255,128,0)
                    elif r < (9/10.0):
                        color = (255,0,0)
                    else:
                        color = (255,255,255)
                    '''
                    #==========WOOD GRAIN==================================================================================================
                    '''
                    r = r*20
                    r = r - int(r)
                    color = (255)*np.array((r,r/2,r/4))
                    '''
                    #============DIFFERENT TOPOLOGICAL MAP =================================================================================
                    '''
                    r = r*20
                    r = r - int(r)
                    color = (255)*np.array((0,r,0))
                    '''
                    #============MARBLE =================================================================================
                    '''
                    r = math.fabs(math.cos(4*r+lx+ly))
                    color = (255)*np.array((r,r,r))
                    '''
                    
                    
                    background.fill(color, ((x,y),(pixelsize,pixelsize)))
                    
                    #draw background into screen
                    screen.blit(background, (0,0))
                    pygame.display.flip()
                    if handleInput(screen):
                        return
                    
                    r = 0
                            
            pixelsize /= 2
            if pixelsize == 0:
                print"Done loading image\n"
            #exp = exp +1
        if handleInput(screen):
            return
            


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
