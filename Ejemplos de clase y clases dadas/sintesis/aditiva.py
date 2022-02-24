#  sintesis aditiva con tabla de armonicos y volumenes

import pyaudio, kbhit, os
import numpy as np

p = pyaudio.PyAudio()

RATE = 44100       # sampling rate, Hz, must be integer
CHUNK = 1024


# frecuencia dada, frame inical, volumen
def osc(frec,vol,frame):
    return (vol*np.sin(2*np.pi*(np.arange(CHUNK)+frame)*frec/RATE)).astype(np.float32)
    





# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=RATE,
                output=True)


kb = kbhit.KBHit()
c = ' '
frec = 440
frame = 0


step = 5
vols = [0.3, 0.2, 0.15, 0.15, 0.1, 0.1]

print("[F/f] subir/bajar frecuencia")

while True:
    arms = [frec*(i+1) for i in range(len(vols))]
    samples = np.zeros(CHUNK,dtype=np.float32)
   
    for i in range(len(vols)):
        samples = samples+osc(arms[i],vols[i],frame)

    stream.write(samples.tobytes()) 
   
    frame += CHUNK

    if kb.kbhit():
        #os.system('clear')
        c = kb.getch()
        print(c)
        if c =='q': break
        elif c=='F': frec=frec+step
        elif c=='f': frec=frec-step
        print("Frec: ", frec)
        for i in range(len(vols)): print("Frec ",arms[i],"  ",vols[i])


stream.stop_stream()
stream.close()

p.terminate()
