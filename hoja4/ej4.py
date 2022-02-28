# sintesis fm con multiples moduladores

import pyaudio, kbhit, os
import numpy as np
# creacion de una ventana de pygame
import pygame
from pygame.locals import *

p = pyaudio.PyAudio()

RATE = 44100       # sampling rate, Hz, must be integer
CHUNK = 16
WIDTH = 64
HEIGHT = 480

class OscWaveTable:
    def __init__(self, frec, vol, size):
        self.frec = frec
        self.vol = vol
        self.size = size
        # un ciclo completo de seno en [0,2pi)
        t = np.linspace(0, 1, num=size)
        self.waveTable = np.sin(2 * np.pi * t)
        # arranca en 0
        self.fase = 0
        # paso en la wavetable en funcion de frec y RATE
        self.step = self.size/(RATE/self.frec)

    def setFrec(self,frec): 
        self.frec = frec
        self.step = self.size/(RATE/self.frec)

    def getFrec(self): 
        return self.frec    


    def getChunk(self):
        samples = np.zeros(CHUNK,dtype=np.float32)
        cont = 0
        #print("RATE ",RATE, "   frec ",self.frec)
        
        while cont < CHUNK:
            self.fase = (self.fase + self.step) % self.size

            # con truncamiento, sin redondeo
            # samples[cont] = self.waveTable[int(self.fase)]

            # con redondeo
            #x = round(self.fase) % self.size
            #samples[cont] = self.waveTable[x]
                        
            # con interpolacion lineal                                    
            x0 = int(self.fase) % self.size
            x1 = (x0 + 1) % self.size
            y0, y1 = self.waveTable[x0], self.waveTable[x1]            
            samples[cont] = y0 + (self.fase-x0)*(y1-y0)/(x1-x0)


            cont = cont+1
        

        return self.vol*samples


# [(fc,vol),(fm1,beta1),(fm2,beta2),...]
def oscFM(frecs,frame):
    # sin(2πfc+βsin(2πfm))  
    chunk = np.arange(CHUNK)+frame
    samples = np.zeros(CHUNK)+frame
    # recorremos en orden inverso
    
    for i in range(len(frecs)-1,-1,-1):
        samples = frecs[i][1] * np.sin(2*np.pi*frecs[i][0]*chunk/RATE + samples)
    return samples

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Theremin")

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=RATE,
                output=True)


kb = kbhit.KBHit()
c = ' '


fc, fm = 220, 220
frecs = [[fc,0.8],[fc+fm,0.5],[fc+2*fm,0.3],[fc+3*fm,0.2]]
frecRange = [100, 10000]
amplitud = [0, 1]

frame = 0

while c != 'q':
    # obtencion de la posicion del raton
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos
            perX, perY = mouseX/float(WIDTH), mouseY/float(HEIGHT)
            frec = frecRange[0] + perX * (frecRange[1] - frecRange[0])
            amp = amplitud[0] + perY * (amplitud[1] - amplitud[0])
            frecs[0][0] = frec
            frecs[0][1] = amp

    samples = oscFM(frecs,frame)
   
    stream.write(samples.astype(np.float32).tobytes()) 
    
    frame += CHUNK

    if kb.kbhit():
        os.system('clear')
        c = kb.getch()
         

pygame.quit()      

stream.stop_stream()
stream.close()

p.terminate()
