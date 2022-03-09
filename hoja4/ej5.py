# EJ5: PIANO POLIFÓNICO
# Daniel Cortijo Gamboa & Tatiana Duarte Balvís

import kbhit, os
import sounddevice as sd   # modulo de conexion con portAudio
import numpy as np
from Nota import Nota

RATE = 44100       # sampling rate, Hz, must be integer
CHUNK = 1024

# abrimos stream de salida
stream = sd.OutputStream(
    samplerate = RATE,  # frec muestreo 
    blocksize  = CHUNK, # tamanio del bloque (muy recomendable unificarlo en todo el programa)
    channels   = 1)     # num de canales

# arrancamos streams
stream.start()

kb = kbhit.KBHit()
c = ' '

# tabla con ruido
size = CHUNK//2  # variar size

# escala diatónica (ABCDEFG)
escala = [440, 493.88, 554.36, 587.33, 659.26, 739.99, 830.61]
teclado = "zxcvbnm"
notas = [] # lista de notas en reproduccion

while c != 'q':
    notaFinal = np.zeros(CHUNK)
    notasRemove = []

    for nota in notas:
        newChunk, fin = nota.newChunk()
        if fin:
            notasRemove.append(nota)
            newChunk = np.append(newChunk, np.zeros(CHUNK - newChunk.shape[0]))
        notaFinal += newChunk

    stream.write(np.float32(notaFinal))

    for nota in notasRemove:
        notas.remove(nota)

    # INPUT
    if kb.kbhit():
        c = kb.getch()    
        index = teclado.find(c) #obtenemos la nota en la escala
        if index != -1:
            notas.append(Nota(CHUNK, escala[index], 0.3*RATE))
    

stream.stop()