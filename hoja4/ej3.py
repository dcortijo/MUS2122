# EJ3: THEREMIN
# Daniel Cortijo Gamboa & Tatiana Duarte Balvís
import kbhit, os
import sounddevice as sd   # modulo de conexion con portAudio
import numpy as np
# creacion de una ventana de pygame
import pygame
from pygame.locals import *

RATE = 44100       # sampling rate, Hz, must be integer
CHUNK = 16
WIDTH = 500
HEIGHT = 500

# [(fc,vol),(fm1,beta1),(fm2,beta2),...]
def oscFM(frecs,frame):
    # sin(2πfc+βsin(2πfm))  
    chunk = np.arange(CHUNK)+frame
    samples = np.zeros(CHUNK)+frame
    # recorremos en orden inverso
    
    for i in range(len(frecs)-1,-1,-1):
        samples = frecs[i][1] * np.sin(2*np.pi*frecs[i][0]*chunk/RATE + samples)
    return samples


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Theremin")

# abrimos stream de salida
stream = sd.OutputStream(
    samplerate = RATE,            # frec muestreo 
    blocksize  = CHUNK,            # tamanio del bloque (muy recomendable unificarlo en todo el programa)
    channels   = 1)  # num de canales

# arrancamos stream
stream.start()

kb = kbhit.KBHit()
c = ' '

fc, fm = 100, 100
frecs = [[fc,0.8],[fc+fm,0.5],[fc+2*fm,0.3],[fc+3*fm,0.2]]
frecRange = [100, 10000]
amplitud = [0, 1]

frame = 0

while c != 'q':
    # obtencion de la posicion del raton
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos
            perX, perY = mouseX/float(WIDTH), 1 - mouseY/float(HEIGHT)  # Para que hacia arriba sea volumen 1
            frec = frecRange[0] + perX * (frecRange[1] - frecRange[0])
            amp = amplitud[0] + perY * (amplitud[1] - amplitud[0])
            frecs[0][0] = frec
            frecs[0][1] = amp

    samples = oscFM(frecs, frame)
   
    stream.write(samples.astype(np.float32)) 
    
    frame += CHUNK

    if kb.kbhit():
        # os.system('clear')    # No lo reconoce
        c = kb.getch()
         

pygame.quit()      

stream.stop()