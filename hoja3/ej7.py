# reproductor con Chunks

from ast import parse
import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import format_tools as ft
import kbhit               # para lectura de teclas no bloqueante

CHUNK = 1024
SRATE = 44100.0
VOL = 1.0

# returns a sinusoidal signal with frec, dur, vol
def osc(frec, dur, vol):
    # number of samples requiered according to SRATE
    nSamples = int(SRATE*dur)
    return vol * np.sin(2*np.pi*np.arange(nSamples)*frec/SRATE)

# def readPartitura(filename):
#     f = open(filename, "r")

def parsePartitura(data, partitura):
    for tup in partitura:
        note = tup[0]
        dur = tup[1]
        data = np.append(data, osc(notas[note], dur * 0.95, VOL))
        data = np.append(data, osc(notas[note], dur * 0.05, 0.0))
    return data

notas = {"C":523.251, "D":587.33, "E":659.255, "F":698.456, "G":789.991, "A":880, "B":987.767,
"c":523.251*2, "d":587.33*2, "e":659.255*2, "f":698.456*2, "g":789.991*2, "a":880*2, "b":987.767*2 }

partitura = [("G", 0.5),("G", 0.5),("A", 1.0),("G", 1.0),
("c", 1.0),("B", 2.0),
("G", 0.5),("G", 0.5),("A", 1.0),("G", 1.0),
("d", 1.0), ("c", 2.0),
("G", 0.5),("G", 0.5),("g", 1.0),("e", 1.0),
("c", 1.0),("B", 1.0),("A", 1.0),
("f", 0.5),("f", 0.5),("e", 1.0),("c", 1.0),
("d", 1.0),("c", 2.0)]

data = np.empty((0, 1), dtype="float32")

data = parsePartitura(data, partitura)
data = ft.toFloat32(data)

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

# termina con 'q' o cuando el último bloque ha quedado incompleto (menos de CHUNK samples)
while c!= 'q' and nSamples==CHUNK: 
    # numero de samples a procesar: CHUNK si quedan sufucientes y si no, los que queden
    nSamples = min(CHUNK,data.shape[0] - (numBloque+1)*CHUNK)

    # nuevo bloque
    bloque = data[numBloque*CHUNK : numBloque*CHUNK+nSamples ]
    bloque *= vol

    # lo pasamos al stream
    stream.write(bloque) # escribimos al stream

    # modificación de volumen 
    if kb.kbhit():
        c = kb.getch()
        if (c=='v'): vol= max(0,vol-0.05)
        elif (c=='V'): vol= min(1,vol+0.05)
        print("Vol: ",vol)

    numBloque += 1
    print('.',end='')


print('end')
stream.stop()
