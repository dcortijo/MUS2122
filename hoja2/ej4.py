#%%
import numpy as np
import matplotlib.pyplot as plt
import numpy.random as rnd

SRATE = 44100

def osc(f, d):
    v = np.arange(SRATE * d, dtype = float)
    for i in np.arange(SRATE * d):
        v[i] = np.sin(2*np.pi * i / SRATE * f)

    plt.figure()
    plt.plot(np.arange(SRATE * d), v, '-', c='purple')
    plt.savefig(f'fig.f{f}.d{d}.png')

    return v

def vol(sample, vol):
    sample *= vol

def modulaVol(sample, frec):
    sample *= frec

v = osc(440, 2)
w = osc(2, 2)

#vol(v, 0.5)
modulaVol(v, w)

plt.figure()
plt.plot(np.arange(SRATE * 2), v, '-', c='blue')
plt.savefig('fig4.v.png')

# %%
