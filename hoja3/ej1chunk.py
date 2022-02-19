#%%
# 1_numPy/playNumPy.py   reproductor con Chunks
import pyaudio, kbhit

import numpy as np  # arrays    
from format_tools import *
import matplotlib.pyplot as plt

SRATE = 44100
CHUNK = 2048
FREC = 440.0
VOL = 1.0

# generadores/oscDinamico2.py
# corregido
last = 0 # ultimo frame generado
def oscChuck(frec,vol):
    global last # var global
    data = vol * np.sin(2 * np.pi * (np.arange(0, CHUNK, dtype = np.float32) + last) * frec / SRATE)
    last += CHUNK # actualizamos ultimo generado
    return data

data = oscChuck(FREC, VOL)

# arrancamos pyAudio
p = pyaudio.PyAudio()

CHUNK = 1024
stream = p.open(format=p.get_format_from_width(getWidthData(data)),
                channels=len(data.shape),
                rate=SRATE,
                frames_per_buffer=CHUNK,
                output=True)


# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
bloque = np.arange(CHUNK,dtype=data.dtype)
numBloque = 0
kb = kbhit.KBHit()
c= ' '
while len(bloque>0) and c!= 'q': 
    # nuevo bloque
    bloque = oscChuck(FREC, VOL)    

    # pasamos al stream  haciendo conversion de tipo 
    stream.write(bloque.astype(data.dtype).tobytes())

    if kb.kbhit():
        c = kb.getch()
        if(c == 'F'):
            FREC += 0.25
        elif(c == 'f'):
            FREC -= 0.25
            if(FREC <= 0):
                FREC = 0.25

    print('.', end='')

kb.set_normal_term()        
stream.stop_stream()
stream.close()
p.terminate()

# ITER = 100

# v = oscChuck(FREC, VOL)
# for i in np.arange(ITER - 1):
#     v = np.append(v, oscChuck(FREC, VOL))

# plt.figure()
# plt.plot(np.arange(CHUNK * ITER), v, '-', c='red')
# plt.savefig("fig{0}.png".format(ITER))
# %%
