# sintesis aditiva + envolvente ADSR


import pyaudio, kbhit, os
import numpy as np

p = pyaudio.PyAudio()

RATE = 44100       # sampling rate, Hz, must be integer
CHUNK = 2048


# frecuencia dada, frame inical, volumen
def osc(frec,vol,frame):
    return (vol*np.sin(2*np.pi*(np.arange(CHUNK)+frame)*frec/RATE)).astype(np.float32)
    

def timeToFrame(t): return int(t*RATE)

def env(lst):
    # convertimos ultimo t de la envolvente en last frame
    last = timeToFrame(lst[len(lst)-1][0])

    # aniadimos 0 al final para evitar el corte con la señal a la que se aplique
    last = last + CHUNK  
     
    # señal con ceros 
    samples = np.zeros(last, dtype=np.float32)
    for i in range(1,len(lst)):
        ''' Interpolación entre cada pareja de puntos (f1,v1) (f2,v2)
        Fórmula clasica ...
        '''        
        f1, f2 = timeToFrame(lst[i-1][0]), timeToFrame(lst[i][0])
        v1, v2 = lst[i-1][1], lst[i][1]
        for j in range(f1,f2):
            # samples  interpolados
            samples[j] = v1 + (j-f1) * (v2-v1)/(f2-f1)
    return samples


# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=RATE,
                output=True)


kb = kbhit.KBHit()
c = ' '
frec = 440
frame = 0



vols = [0.3, 0.2, 0.15, 0.15, 0.1, 0.1]

ptosEnv = [(0,0),(0.02,0.9),(0.1,0.3),(0.6,0.2),(2.3,0)]
last = len(ptosEnv)-1
endFrame = timeToFrame(ptosEnv[last][0])

envSamples = env(ptosEnv) 


frame = 0
while frame<endFrame:

    samples = np.zeros(CHUNK,dtype=np.float32)   
    
    arms = [frec*(i+1) for i in range(len(vols))]
    for i in range(len(vols)):
        samples = samples+osc(arms[i],vols[i],frame)
    
    samples = samples * envSamples[frame:frame+CHUNK]
    frame += CHUNK
    
    stream.write(samples.tobytes()) 




stream.stop_stream()
stream.close()

p.terminate()
