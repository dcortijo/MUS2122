def sqrChuck(frec,vol):
    global last # var global
    data = vol*sc.square(2*np.pi*(np.arange(CHUNK)+last)*frec/SRATE)
    last += CHUNK # actualizamos ultimo generado
    return data

def triChuck(frec,vol):
    global last # var global
    data = vol*np.tri(2*np.pi*(np.arange(CHUNK)+last)*frec/SRATE)
    last += CHUNK # actualizamos ultimo generado
    return data

def sawChuck(frec,vol):
    global last # var global
    data = vol*np.sin(2*np.pi*(np.arange(CHUNK)+last)*frec/SRATE)
    last += CHUNK # actualizamos ultimo generado
    return data