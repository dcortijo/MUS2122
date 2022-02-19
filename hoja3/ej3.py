#%%
# 1_numPy/playNumPy.py   reproductor con Chunks
import pyaudio, kbhit

import numpy as np  # arrays    
from format_tools import *
import matplotlib.pyplot as plt
import scipy.signal as sc

SRATE = 44100
CHUNK = 2048
FREC = 440.0
VOL = 1.0
MFREC = 2.0
MVOL = 1.0

# generadores/oscDinamico2.py
# corregido
last = 0 # ultimo frame generado
def oscChuck(frec,vol):
    global last # var global
    data = vol * np.sin(2 * np.pi * (np.arange(0, CHUNK, dtype = np.float32) + last) * frec / SRATE)
    last += CHUNK # actualizamos ultimo generado
    return data

def sqrChuck(frec,vol):
    global last # var global
    data = vol*sc.square(2*np.pi*(np.arange(CHUNK)+last)*frec/SRATE)
    last += CHUNK # actualizamos ultimo generado
    return data

def triChuck(frec,vol):
    global last # var global
    data = vol*sc.sawtooth(2*np.pi*(np.arange(CHUNK)+last)*frec/SRATE)  # Podriamos hacer una nosotros pero uff
    last += CHUNK # actualizamos ultimo generado
    return data

def sawChuck(frec,vol):
    global last # var global
    data = vol*sc.sawtooth(2*np.pi*(np.arange(CHUNK)+last)*frec/SRATE)
    last += CHUNK # actualizamos ultimo generado
    return data

def modOscChuck(frec, vol):
    global last # var global
    data = vol * np.sin(2 * np.pi * (np.arange(0, CHUNK, dtype = np.float32) + last) * frec / SRATE)
    return data

def moduladorAmplitud(wave, frec, vol):
    return wave * ((modOscChuck(frec, vol) / 2.0) + 0.5) # De 0 a 1

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
    bloque = moduladorAmplitud(bloque, MFREC, MVOL)

    # pasamos al stream  haciendo conversion de tipo 
    stream.write(bloque.astype(data.dtype).tobytes())

    if kb.kbhit():
        c = kb.getch()

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