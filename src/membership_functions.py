import numpy as np

def dsigmf(x, b1, c1, b2, c2):
    def f1(x):
        return 1 / (1. + np.exp(- c1 * (x - b1)))
    
    def f2(x):
        return 1 / (1. + np.exp(- c2 * (x - b2)))

    return f1(x) - f2(x)

def sigmf(x, b, c):
    return 1 / (1. + np.exp(- c * (x - b)))
