import numpy as np

def gaussian( x, mu, sig ):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def linear( x, k, c ):
    return k * x + c
