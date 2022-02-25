# EJ 10: IDIOTIZADOR

from Delay import Delay
import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexion con portAudio
import kbhit               # para lectura de teclas no bloqueante

CHUNK = 1024    # tamaño de bloque
SRATE = 44100   # sapling rate
DELAY = 2       # segundos de retardo
CHANNELS = 1    # canales en delay y los streams

delayed = Delay(SRATE, CHANNELS, DELAY)

# abrimos stream de salida
outputStream = sd.OutputStream(
    samplerate = SRATE,            # frec muestreo 
    blocksize  = CHUNK,            # tamanio del bloque (muy recomendable unificarlo en todo el programa)
    channels   = CHANNELS)         # num de canales

# arrancamos stream
outputStream.start()

# abrimos stream de entrada (InpuStream)
inputStream = sd.InputStream(samplerate=SRATE, blocksize=CHUNK, dtype="float32", channels=CHANNELS)

# arrancamos stream
inputStream.start()

# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
kb = kbhit.KBHit()
c= ' '

# termina con 'q' o cuando el ultimo bloque ha quedado incompleto (menos de CHUNK samples)
while c!= 'q': 
    # nuevo bloque
    bloque = inputStream.read(CHUNK)

    # Aniadimos lo leido al delay 
    delayedBlock = delayed.addChunk(bloque[0]) # y recogemos lo que delayeado

    # lo pasamos al stream
    outputStream.write(np.float32(delayedBlock)) # escribimos al stream

    print('.',end='')

print('end')
outputStream.stop()
