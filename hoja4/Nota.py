# EJ 5: PIANO POLÍFONICO    
# Daniel Cortijo Gamboa & Tatiana Duarte Balvís

import numpy as np

def karplus_strong(wavetable, nSamples):
    """Synthesizes a new waveform from an existing wavetable, modifies last sample by averaging."""
    samples = []
    current_sample = 0
    previous_value = 0
    while len(samples) < nSamples:
        wavetable[current_sample] = 0.5 * (wavetable[current_sample] + previous_value)
        samples.append(wavetable[current_sample])
        previous_value = samples[-1]
        current_sample += 1
        current_sample = current_sample % wavetable.size
    return np.array(samples)

class Nota:
    def __init__(self, chunk, frec, dur):
        self.chunk = chunk
        self.frec = frec
        self.dur = dur
        self.wavetable = 2 * np.random.randint(0, 2, int(frec) - 1).astype(np.float32)
        self.nota = karplus_strong(self.wavetable, self.dur)
        self.start = 0
            
    def newChunk(self):
        size = np.shape(self.nota)[0]
        aux = size - self.start
        if (aux > self.chunk):
            aux = self.chunk

        returnChunk = np.copy(self.nota[ self.start : self.start + aux])
        self.start = self.start + aux

        return returnChunk, (self.start == size)