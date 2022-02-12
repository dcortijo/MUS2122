#%%
import numpy as np
import matplotlib.pyplot as plt
import numpy.random as rnd

v = np.arange(44100, dtype = float)
for i in np.arange(44100):
    v[i] = rnd.random_sample() - rnd.random_sample()

print(v)

plt.figure()
plt.plot(np.arange(44100), v, '-', c='purple')
plt.savefig('fig1.png')
# %%
