#%%
# 1_numPy/playNumPy.py   reproductor con Chunks
import chunk
from copy import copy
import pyaudio, kbhit

import numpy as np  # arrays    
from format_tools import *
from scipy.io import wavfile # para manejo de wavs

# abrimos wav y recogemos frecMuestreo y array de datos
SRATE, data = wavfile.read('piano.wav')
data = toFloat32(data)

# informacion de wav
print("Sample rate ",SRATE)
print("Sample format: ",data.dtype)
print("Num channels: ",len(data.shape))
print("Len: ",data.shape[0])

# arrancamos pyAudio
p = pyaudio.PyAudio()

CHUNK = 1024
stream = p.open(format=p.get_format_from_width(getWidthData(data)),
                channels=2,
                rate=SRATE,
                frames_per_buffer=CHUNK,
                output=True)

def modOscChuck(frec, vol):
    global numBloque # var global
    data = vol * np.sin(2 * np.pi * (np.arange(0, CHUNK, dtype = np.float32) + (numBloque * CHUNK)) * frec / SRATE)
    return data

multiplier = 1  # Esto es para que no sea demasiado brusco, con suavizado
def balance(bloque):
    oscilador = modOscChuck(5.0, 1.0)
    izq = np.copy(bloque)
    der = np.copy(bloque)
    for i in np.arange(np.shape(bloque)[0]):
        der[i] *= ((oscilador[i]/-2.0) + 0.5)
        izq[i] *= ((oscilador[i]/2.0) + 0.5)
    bloque = np.hstack((der.reshape(-1, 1), izq.reshape(-1,1)))
    return bloque

# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
bloque = np.arange(CHUNK,dtype=data.dtype)
numBloque = 0
kb = kbhit.KBHit()
c= ' '
while len(bloque>0) and c!= 'q': 
    # nuevo bloque
    bloque = data[ numBloque*CHUNK : numBloque*CHUNK+CHUNK ] 
    if(np.shape(bloque)[0] > 0):
        bloque = balance(bloque)

    # pasamos al stream  haciendo conversion de tipo 
    stream.write(bloque.astype(data.dtype).tobytes())

    if kb.kbhit():
        c = kb.getch()

    numBloque += 1
    print('.', end='')

kb.set_normal_term()        
stream.stop_stream()
stream.close()
p.terminate()
# %%