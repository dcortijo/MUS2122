# EJ 9: DELAY
# Daniel Cortijo Gamboa & Tatiana Duarte Balvís
from Delay import Delay
import numpy as np         # arrays    
import sounddevice as sd
import kbhit               # para lectura de teclas no bloqueante

CHUNK = 1024
SRATE = 44100
VOL = 1.0
DELAY = 2   # duracion del delay en segundos
OSCDUR = 5  # duracion del sonido en segundos
CHANNELS = 1

# devuelve una senial sinusoidal con frecuencia frec, duracion dur y volumen vol
def osc(frec, dur, vol):
    # numero de samples necesarios segun srate
    nSamples = int(SRATE*dur)
    return vol * np.sin(2*np.pi*np.arange(nSamples)*frec/SRATE)

# generamos onda
data = osc(880, OSCDUR, VOL)
data = np.reshape(data, newshape=(np.shape(data)[0], CHANNELS)) # Hacemos esto ya que Delay necesita que haya por lo menos 1 shape (x, 1)

delayed = Delay(SRATE, CHANNELS, DELAY)

# abrimos stream de salida
stream = sd.OutputStream(
    samplerate = SRATE,            # frec muestreo 
    blocksize  = CHUNK,            # tamanio del bloque (muy recomendable unificarlo en todo el programa)
    channels   = CHANNELS)  # num de canales

# arrancamos stream
stream.start()

# En data tenemos la onda generada, ahora procesamos por chunks
numBloque = 0
kb = kbhit.KBHit()
c= ' '

timer = 0
nSamples = CHUNK 
print('\n\nProcessing chunks: ',end='')

# termina con 'q' o cuando el ultimo bloque ha quedado incompleto (menos de CHUNK samples)
while c!= 'q' and timer < (DELAY * SRATE) + np.shape(data)[0]: # Para tras acabar la duraciñón del delay y la nota
    # nuevo bloque
    bloque = data[numBloque*CHUNK : numBloque*CHUNK+nSamples]
    if np.shape(bloque)[0] == 0: 
        bloque = np.zeros(shape=(CHUNK, 1))

    delayedBlock = delayed.addChunk(bloque) # Aniade el chunk y devuelve el que le corresponde con el retraso

    # lo pasamos al stream
    stream.write(np.float32(delayedBlock)) # escribimos al stream

    # numero de samples a procesar: CHUNK si quedan sufucientes y si no, los que queden
    nSamples = min(CHUNK, delayedBlock.shape[0])

    # entrada por teclado
    if kb.kbhit():
        c = kb.getch()

    timer += np.shape(delayedBlock)[0]

    numBloque += 1
    print('.',end='')

print('end')
stream.stop()