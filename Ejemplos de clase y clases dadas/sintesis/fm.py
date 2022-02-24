# sintesis fm con osciladores variables

import pyaudio, kbhit, os
import numpy as np

p = pyaudio.PyAudio()

RATE = 44100       # sampling rate, Hz, must be integer
CHUNK = 16


# fc, carrier = pitch, fm frecuencia moduladora, beta = indice de modulacion
def oscFM(fc,fm,beta,vol,frame):
    # sin(2πfc+βsin(2πfm))   http://www.mrcolson.com/2016/04/21/Simple-Python-FM-Synthesis.html
    sample = np.arange(CHUNK)+frame
    mod = beta*np.sin(2*np.pi*fm*sample/RATE)
    res = np.sin(2*np.pi*fc*sample/RATE + mod)
    return vol*res
    


# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=RATE,
                output=True)


kb = kbhit.KBHit()
c = ' '

fc = 440
fm = 300
beta = 1
vol = 0.8
frame = 0

while True:
    samples = oscFM(fc,fm,beta,vol,frame)
   
    stream.write(samples.astype(np.float32).tobytes()) 
    
    frame += CHUNK

    if kb.kbhit():
        os.system('clear')
        c = kb.getch()
        print(c)        
        if c =='q': break
        elif c=='C': fc += 1
        elif c=='c': fc -= 1    
        elif c=='M': fm += 1    
        elif c=='m': fm -= 1            
        elif c=='B': beta += 0.1    
        elif c=='b': beta -= 0.1            

        print("[C/c] Carrier (pitch): ", fc)
        print("[M/m] Frec moduladora: ", fm)
        print("[B/b] Factor (beta): ",beta)
        print("q quit")


stream.stop_stream()
stream.close()

p.terminate()
