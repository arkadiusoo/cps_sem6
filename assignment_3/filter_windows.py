import numpy as np

def rectangular_window(M):
    return np.ones(M)

def hanning_window(M):
    n = np.arange(M)
    return 0.5 - 0.5 * np.cos(2 * np.pi * n / (M - 1))

def get_window_function(name, M):

    if name == "rectangular":
        return rectangular_window(M)
    elif name == "hanning":
        return hanning_window(M)
    else:
        raise ValueError(f"Unsupported window type: {name}")
