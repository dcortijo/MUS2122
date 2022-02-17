# 1_numPy/playNumPy.py   reproductor con Chunks
#import pyaudio, kbhit

import numpy as np  # arrays    
from format_tools import *
import matplotlib.pyplot as plt
import time

SRATE = 44100
CHUNK = 2048
FREC = 100.0
VOL = 10.0

# generadores/oscDinamico2.py
# corregido
last = 0 # ultimo frame generado
def oscChuck(frec,vol):
    global last # var global
    data = vol * np.sin(2 * np.pi * (np.arange(0, CHUNK, dtype = np.float32) + last) * frec / SRATE)
    last += CHUNK # actualizamos ultimo generado
    return data

#data = oscChuck(FREC, VOL)

# arrancamos pyAudio
#p = pyaudio.PyAudio()

# numBloque = 0
# def callback(in_data, frame_count, time_info, status):
#     #  frame_count: numero de frames que hay que devolver
#     #  frame_count = frames_per_buffer = CHUNK
#     global numBloque
#     print("Callback bloque ", numBloque, "fc ", frame_count, FREC)
#     bloque = oscChuck(FREC, VOL)
#     numBloque += 1
#     return (bloque, pyaudio.paContinue)
    
# stream = p.open(format=p.get_format_from_width(getWidthData(data)),
#                 channels=len(data.shape),
#                 rate=SRATE,
#                 frames_per_buffer = CHUNK,
#                 output=True,
#                 stream_callback=callback)

# # start the stream (4)
# stream.start_stream()

# kb = kbhit.KBHit()
# c= ' '
# # wait for stream to finish (5)
# while stream.is_active() and c!= 'q':
#     if kb.kbhit():
#         c = kb.getch()
#         if(c == 'F'):
#             FREC += 0.25
#         elif(c == 'f'):
#             FREC -= 0.25
#             if(FREC <= 0):
#                 FREC = 0.25
#     time.sleep(1)

v = oscChuck(FREC, VOL)
v = np.append(v, oscChuck(FREC, VOL))
FREC *= 1.5
v = np.append(v, oscChuck(FREC, VOL))
v = np.append(v, oscChuck(FREC, VOL))
plt.figure()
plt.plot(np.arange(CHUNK * 4), v, '-', c='purple')
plt.savefig('fig1.png')

print("fin")
# stop stream (6)
# stream.stop_stream()
# stream.close()
#wf.close()

# close PyAudio (7)
# p.terminate()
# %%
