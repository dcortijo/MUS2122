# EJ 7: HAPPY BIRTHDAY (sin parte opcional)
# Daniel Cortijo Gamboa & Tatiana Duarte Balvís
from ast import parse
import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexion con portAudio
import format_tools as ft
import kbhit               # para lectura de teclas no bloqueante

CHUNK = 1024
SRATE = 44100.0
VOL = 1.0
SECS_PER_UNIT = 1.0 # para establñecer segundos/negra

# devuelve una senial sinusoidal con frecuencia frec, duracion dur y volumen vol
def osc(frec, dur, vol):
    # numero de samples necesarios segun srate
    nSamples = int(SRATE*dur)
    return vol * np.sin(2*np.pi*np.arange(nSamples)*frec/SRATE)


# convierte las notas de una partitura en una senial
def parsePartitura(data, partitura):
    for tup in partitura:
        note = tup[0]
        dur = tup[1]
        data = np.append(data, osc(notas[note], dur * SECS_PER_UNIT * 0.95, VOL))
        # forzamos un pequeño silencio entre cada nota para separarlas
        data = np.append(data, osc(notas[note], dur * SECS_PER_UNIT * 0.05, 0.0)) 
    return data

# Frecuencias de notas
notas = {"C":523.251, "D":587.33, "E":659.255, "F":698.456, "G":789.991, "a":880, "b":987.767,
        "c":523.251*2, "d":587.33*2, "e":659.255*2, "f":698.456*2, "g":789.991*2, "a'":880*2, "b'":987.767*2 }

# Partitura hardcoded
partitura = [("G", 0.5),("G", 0.5),("a", 1.0),("G", 1.0),
            ("c", 1.0),("b", 2.0),
            ("G", 0.5),("G", 0.5),("a", 1.0),("G", 1.0),
            ("d", 1.0), ("c", 2.0),
            ("G", 0.5),("G", 0.5),("g", 1.0),("e", 1.0),
            ("c", 1.0),("b", 1.0),("a", 1.0),
            ("f", 0.5),("f", 0.5),("e", 1.0),("c", 1.0),
            ("d", 1.0),("c", 2.0)]

data = np.empty((0, 1))
data = parsePartitura(data, partitura)

# abrimos stream de salida
stream = sd.OutputStream(
    samplerate = SRATE,            # frec muestreo 
    blocksize  = CHUNK,            # tamanio del bloque (muy recomendable unificarlo en todo el programa)
    channels   = len(data.shape))  # num de canales

# arrancamos stream
stream.start()

numBloque = 0
kb = kbhit.KBHit()
c= ' '

vol = 1.0
nSamples = CHUNK 
print('\n\nProcessing chunks: ', end='')

# termina con 'q' o cuando el ultimo bloque ha quedado incompleto (menos de CHUNK samples)
while c!= 'q' and nSamples==CHUNK: 
    # numero de samples a procesar: CHUNK si quedan sufucientes y si no, los que queden
    nSamples = min(CHUNK, data.shape[0] - (numBloque+1) * CHUNK)

    # nuevo bloque
    bloque = data[numBloque*CHUNK : numBloque*CHUNK + nSamples ]
    bloque *= vol

    # lo pasamos al stream
    stream.write(np.float32(bloque)) # escribimos al stream

    # entrada por teclado
    if kb.kbhit():
        c = kb.getch()

    numBloque += 1
    print('.', end='')

print('end')
stream.stop()