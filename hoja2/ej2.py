#%%
import numpy as np
import matplotlib.pyplot as plt
import numpy.random as rnd

v = np.arange(44100, dtype = float)
for i in np.arange(44100):
    v[i] = np.sin(2*np.pi * i / 44100)

plt.figure()
plt.plot(np.arange(44100), v, '-', c='purple')
plt.savefig('fig2.png')

for i in np.arange(44100):
    v[i] = np.sin(2*np.pi * i / 44100.0 * 2)

plt.figure()
plt.plot(np.arange(44100), v, '-', c='purple')
plt.savefig('fig2.1.png')

v = np.arange(88200, dtype = float)
for i in np.arange(88200):
    v[i] = np.sin(2*np.pi * i / 44100 * 3)

plt.figure()
plt.plot(np.arange(88200), v, '-', c='purple')
plt.savefig('fig2.2.png')
# %%
