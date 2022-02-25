import numpy as np         # arrays    

class Delay:
    def __init__(self, srate, channelnum, initalsilence): 
        self.samplerate = srate # sample rate
        self.buffer = np.zeros(shape=(int(initalsilence * srate), channelnum) )   # Crea un silencio inicial con un numero de canales por parametro
        self.start = 0  # por que chunk empieza ahora

    def addChunk(self, chunk):
        chunkSize = np.shape(chunk)[0]
        buffSize = np.shape(self.buffer)[0]
        firstSize = np.min([buffSize - self.start, chunkSize])
        secondSize = chunkSize - firstSize

        returnChunk = np.copy(self.buffer[ self.start  : self.start + firstSize ])
        self.buffer[ self.start  : self.start + firstSize ] = chunk[ 0 : firstSize]
        self.start = (self.start + firstSize) % buffSize

        if secondSize > 0:
            returnChunk = np.append(returnChunk, np.copy(self.buffer[ self.start  : self.start + secondSize ]))
            self.buffer[ self.start  : self.start + secondSize ] = chunk[ firstSize : ]
            self.start = (self.start + secondSize) % buffSize

        return returnChunk