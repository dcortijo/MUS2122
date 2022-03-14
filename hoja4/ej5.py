# EJ5: PIANO POLIFÓNICO
# Daniel Cortijo Gamboa & Tatiana Duarte Balvís

from sympy import maximum
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

    counter = 0 # Si no no se oye bien

    for nota in notas:

        counter = counter + 1 # Si no no se oye bien

        newChunk, fin = nota.newChunk()
        if fin:
            notasRemove.append(nota)
            newChunk = np.append(newChunk, np.zeros(CHUNK - newChunk.shape[0]))
        notaFinal += newChunk
    
    if(counter > 0): notaFinal = notaFinal / counter # Si no no se oye bien

    stream.write(np.float32(notaFinal))

    for nota in notasRemove:
        notas.remove(nota)

    # INPUT
    if kb.kbhit():
        c = kb.getch()    
        index = teclado.find(c) #obtenemos la nota en la escala
        if index != -1:
            notas.append(Nota(CHUNK, escala[index], RATE))

stream.stop()

# Tuvimos que dividir entre el numero de notas, ya que si no lo haciamos se oia
# mal si juntabamos dos notas. No sabemos por que podria ser, si era porque superaba
# un umbral de aplitud o algo similar, pero no conseguimos arreglarlo