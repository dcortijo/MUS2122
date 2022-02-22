import numpy as np         # arrays    

class Delay:
    def __init__(self, chunk, srate, channelnum, initalsilence): 
        self.chunkSize = chunk   # tamanio de bloque
        self.samplerate = srate # sample rate
        self.buffer = np.zeros((int(initalsilence * srate), channelnum), dtype="float32")    # Crea un silencio inicial con un numero de canales por parametro
        self.numBloque = 0  # por que chunk

    def addChunk(self, chunk):
        self.buffer = np.append(self.buffer, chunk)

    def retrieveChunk(self):
        # if((self.numBloque + 1) * self.chunkSize > np.shape(self.buffer)[0]):
        #     chunk = self.buffer[ self.numBloque * self.chunkSize : np.shape(self.buffer)[0] - self.numBloque * self.chunkSize ] # si no es un bloque entero ?
        # else:                                                                                                                   # esto esta bien o es necesario ?
        #    chunk = self.buffer[ self.numBloque * self.chunkSize : (self.numBloque + 1) * self.chunkSize ]  # si puede coger un bloque entero 
        chunk = self.buffer[ self.numBloque * self.chunkSize : (self.numBloque + 1) * self.chunkSize ] 
        self.numBloque = self.numBloque + 1
        return chunk