# EJ 9: DELAY
# Daniel Cortijo Gamboa & Tatiana Duarte Balvís
import numpy as np         # arrays    

class Delay:
    def __init__(self, srate, channelnum, initalsilence): 
        self.samplerate = srate     # sample rate
        self.buffer = np.zeros(shape=(int(initalsilence * srate), channelnum) )   # Crea un silencio inicial con un numero de canales por parametro
        self.start = 0              # por que chunk empieza ahora

    def addChunk(self, chunk):
        chunkSize = np.shape(chunk)[0]  # Tamanio de lo que vamos a aniadir
        buffSize = np.shape(self.buffer)[0] # tamanio del buffer
        firstSize = np.min([buffSize - self.start, chunkSize])  # vemos si sobresale por la derecha del buffer
        secondSize = chunkSize - firstSize

        returnChunk = np.copy(self.buffer[ self.start  : self.start + firstSize ])  # copiamos la primera parte
        self.buffer[ self.start  : self.start + firstSize ] = chunk[ 0 : firstSize] # sustituimos la parte que hemos copiado por el chunk
        self.start = (self.start + firstSize) % buffSize    # ajustamos por que parte del buffer se empieza ahora

        if secondSize > 0: # repite el mismo proceso, por si ha sobresalido por la derecha y hemos vuelto por la izquierda
            returnChunk = np.append(returnChunk, np.copy(self.buffer[ self.start  : self.start + secondSize ]))
            self.buffer[ self.start  : self.start + secondSize ] = chunk[ firstSize : ]
            self.start = (self.start + secondSize) % buffSize

        return returnChunk