import numpy as np

def manual_convolution(x: list[float], h: list[float]) -> list[float]:
    """Performs manual linear convolution of two signals."""
    N = len(x)
    M = len(h)
    y = [0.0] * (N + M - 1)
    for n in range(N + M - 1):
        for k in range(M):
            if 0 <= n - k < N:
                y[n] += x[n - k] * h[k]
    return y

def library_convolution(x: list[float], h: list[float]) -> list[float]:
    """Performs convolution using numpy."""
    return np.convolve(x, h, mode='full').tolist()