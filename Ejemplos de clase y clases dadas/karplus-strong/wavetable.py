# wavetable sin cambio de frecuencia
# se genera un nuevo wavetable al cambiar la frecuencia, i.e., no es wavetable real


import pyaudio, kbhit, os
import numpy as np

import matplotlib.pyplot as plt

p = pyaudio.PyAudio()

RATE = 44100       # sampling rate, Hz, must be integer
CHUNK = 1024




def synthWaveTable(wavetable, frame):
    samples = np.zeros(CHUNK, dtype=np.float32)
    t = frame % len(wavetable)
    for i in range(CHUNK):
        samples[i] = wavetable[t]
        t = (t+1) % len(wavetable)
    return samples


stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=RATE,
                output=True)


kb = kbhit.KBHit()
c = ' '

vol = 0.8
frame = 0

frec = 800
waveTable = np.sin(2*np.pi*frec*np.arange(RATE/frec,dtype=np.float32)/RATE) 
while True:
    samples = synthWaveTable(waveTable,frame)
   
    stream.write(samples.tobytes()) 
    
    frame += CHUNK

    if kb.kbhit():
        os.system('clear')
        c = kb.getch()
        print(c)        
        if c =='q': break
        elif c=='F': frec = frec+1
        elif c=='f': frec = frec-1
        print("Frec ",frec)
        print("[F/f] subir/bajar frec")
        print("q quit")
        waveTable = np.sin(2*np.pi*frec*np.arange(RATE/frec,dtype=np.float32)/RATE) 


stream.stop_stream()
stream.close()

p.terminate()
