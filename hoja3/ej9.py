# reproductor con Chunks

from Delay import Delay
import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import format_tools as ft
import kbhit               # para lectura de teclas no bloqueante

CHUNK = 1024
SRATE = 44100.0
VOL = 1.0
DELAY = 5

# returns a sinusoidal signal with frec, dur, vol
def osc(frec, dur, vol):
    # number of samples requiered according to SRATE
    nSamples = int(SRATE*dur)
    return vol * np.sin(2*np.pi*np.arange(nSamples)*frec/SRATE)

data = np.empty((0, 1), dtype="float32")

data = np.append(data, osc(440, 1, 1))
data = ft.toFloat32(data)

delayed = Delay(CHUNK, SRATE, data.ndim, DELAY)

# abrimos stream de salida
stream = sd.OutputStream(
    samplerate = SRATE,            # frec muestreo 
    blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
    channels   = len(data.shape))  # num de canales

# arrancamos stream
stream.start()

# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
# bloque = np.arange(CHUNK,dtype=data.dtype)
numBloque = 0
kb = kbhit.KBHit()
c= ' '

vol = 1.0
nSamples = CHUNK 
print('\n\nProcessing chunks: ',end='')

delayedBlock = np.empty((0, 1), dtype="float32")

# termina con 'q' o cuando el último bloque ha quedado incompleto (menos de CHUNK samples)
while c!= 'q' and nSamples==CHUNK: 
    # nuevo bloque
    bloque = data[numBloque*CHUNK : numBloque*CHUNK+nSamples ]
    bloque *= vol

    delayed.addChunk(bloque)
    delayedBlock = delayed.retrieveChunk()

    # lo pasamos al stream
    stream.write(delayedBlock) # escribimos al stream

    # numero de samples a procesar: CHUNK si quedan sufucientes y si no, los que queden
    nSamples = min(CHUNK, delayedBlock.shape[0])

    numBloque += 1
    print('.',end='')

print('end')
stream.stop()
