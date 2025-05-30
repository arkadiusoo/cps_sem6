import numpy as np

from assignment_3.convolution import (manual_convolution)

def correlation_via_convolution(h, x):
    h_reversed = h[::-1]
    return manual_convolution(x, h_reversed)

def manual_correlation(x, y, mode="linear"):

    N = len(x)
    M = len(y)

    if mode == "linear":

        result = []
        for n in range(N + M - 1):
            acc = 0.0
            for k in range(M):
                if 0 <= n - k < N:
                    acc += y[k] * x[n - k]
            result.append(acc)
        print(len(result))
        return result

    elif mode == "circular":

        L = max(N, M)
        x_padded = x + [0] * (L - N)
        y_padded = y + [0] * (L - M)
        result = []
        for n in range(L):
            acc = 0.0
            for k in range(L):
                acc += y_padded[k] * x_padded[(n - k) % L]
            result.append(acc)

        return result

    else:
        raise ValueError("Invalid mode. Use 'linear' or 'circular'.")


def library_correlation(x, y, mode="linear"):

    x = np.array(x)
    y = np.array(y)

    if mode == "linear":
        return np.correlate(x, y, mode="full").tolist()
    elif mode == "circular":
        N = max(len(x), len(y))
        x = np.pad(x, (0, N - len(x)), mode='constant')
        y = np.pad(y, (0, N - len(y)), mode='constant')
        # FFT-based circular correlation: IFFT(FFT(x) * conj(FFT(y)))
        x_fft = np.fft.fft(x)
        y_fft = np.fft.fft(y)
        result = np.fft.ifft(x_fft * np.conj(y_fft)).real
        return result.tolist()
    else:
        raise ValueError("Invalid mode. Use 'linear' or 'circular'.")