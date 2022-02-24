# sintesis aditiva con variacion de volumenes de armónicos y fases programables

import pyaudio, kbhit, os
import numpy as np

p = pyaudio.PyAudio()

RATE = 44100       # sampling rate, Hz, must be integer
CHUNK = 1024


# frecuencia dada, frame inical, volumen
def osc(frec,vol,frame):
    return (vol*np.sin(2*np.pi*(np.arange(CHUNK)+frame)*frec/RATE)).astype(np.float32)
    

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=RATE,
                output=True)


kb = kbhit.KBHit()
c = ' '
frec = 220
frame = 0



vols =   [0.3, 0.2, 0.15, 0.15, 0.1,  0.1,  0.2, 0.1, 0.5, 0.3 ]
delays = [0,  0.04, 0.1,  0.07, 0.03, 0.02, 0,0, 0,   0,   0 ]

while True:
    arms = [frec*(i+1) for i in range(len(vols))]
    samples = np.zeros(CHUNK,dtype=np.float32)
   
    for i in range(len(vols)):
        delay = delays[i]*RATE
        samples = samples+osc(arms[i],vols[i],frame+delay)

    stream.write(samples.tobytes()) 

    
    frame += CHUNK

    if kb.kbhit():
        os.system('clear')
        c = kb.getch()
        print(c)        
        if c =='z': break
        elif c=='Y': frec=frec+step
        elif c=='y': frec=frec-step
        elif (c>='a' and c<='x'):
            v = ord(c)-ord('a')
            if v<len(vols): vols[v] = max(0,vols[v]-0.01)
        elif (c>='A' and c<='X'):
            v = ord(c)-ord('A')
            if v<len(vols): vols[v] = min(1,vols[v]+0.01) 

        print("[Y/y] Frec: ", frec)
        print("z quit")
        for i in range(len(vols)): 
            print("["+str(chr(ord('A')+i))+"/"+str(chr(ord('a')+i))+"] ", " Frec " , arms[i],"  ",vols[i], "  delay: ",delays[i])


stream.stop_stream()
stream.close()

p.terminate()
