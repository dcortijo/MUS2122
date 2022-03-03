# EJ5: PIANO POLIFÓNICO
# Daniel Cortijo Gamboa & Tatiana Duarte Balvís
from operator import contains
import kbhit, os
from karplusStrong import karplus_strong
import sounddevice as sd   # modulo de conexion con portAudio
import numpy as np

RATE = 44100       # sampling rate, Hz, must be integer
CHUNK = 1024
STREAMS = 10

# abrimos stream de salida
streams = np.empty(0)
for i in np.arange(STREAMS):
    streams = np.append(streams, 
    sd.OutputStream(
    samplerate = RATE,            # frec muestreo 
    blocksize  = CHUNK,           # tamanio del bloque (muy recomendable unificarlo en todo el programa)
    channels   = 1))  # num de canales

# arrancamos streams
for i in np.arange(STREAMS):
    streams[i].start()

kb = kbhit.KBHit()
c = ' '

frame = 0

# tabla con ruido
size = CHUNK//2  # variar size

# escala diatónica
escala = [(2 * np.random.randint(0, 2, int(size/2**(k/12))) - 1).astype(np.float32) for k in [0,2,3,5,7,8,10,12]]
keyboard = "zxcvbnm"

while c != 'q':  
    if kb.kbhit():
        c = kb.getch()    
        index = keyboard.find(c)
        if index != -1:
            streams[0].write(karplus_strong(escala[index], 0.3*RATE))

for i in np.arange(STREAMS):
    streams[i].stop()