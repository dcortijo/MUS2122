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

def fadeOut(sample, t):
    ini = SRATE * t
    fin = np.shape(sample)[0]
    w = np.ones(ini)
    v = np.arange(0, 1, 1 / float(fin - ini), dtype = float)
    v = np.flip(v)
    w = np.append(w, v)
    sample *= w

def fadeIn(sample, t):
    ini = 0
    fin = SRATE * t
    w = np.ones(np.shape(sample)[0] - fin)
    v = np.arange(0, 1, 1 / float(fin - ini), dtype = float)
    v = np.append(v, w)
    sample *= v

v = osc(440, 2)
fadeIn(v, 1)

plt.figure()
plt.plot(np.arange(SRATE * 2), v, '-', c='blue')
plt.savefig('fig5.png')

# %%
