#%%
import numpy as np
import matplotlib.pyplot as plt
import numpy.random as rnd

SRATE = 44100

def osc(f, d):
    v = np.arange(SRATE * d, dtype = float)
    # Otra forma: sig = np.sin(v * 2*np.pi * i / SRATE * f)
    for i in np.arange(SRATE * d):
        v[i] = np.sin(2*np.pi * i / SRATE * f)

    plt.figure()
    plt.plot(np.arange(SRATE * d), v, '-', c='purple')
    plt.savefig(f'fig.f{f}.d{d}.png')

    return v
# %%
