import numpy as np


def manual_correlation(x, y, mode="linear"):
    """
    Computes correlation R_xy[k] = sum_n x[n] * y[n - k]
    mode: 'linear' or 'circular'
    """

    x = np.array(x)
    y = np.array(y)

    if mode == "circular":
        N = max(len(x), len(y))
        x = np.pad(x, (0, N - len(x)), mode='constant')
        y = np.pad(y, (0, N - len(y)), mode='constant')
        # FFT-based circular correlation: IFFT(FFT(x) * conj(FFT(y)))
        result = np.fft.ifft(np.fft.fft(x) * np.conj(np.fft.fft(y))).real
    elif mode == "linear":
        result = np.correlate(x, y, mode='full')
    else:
        raise ValueError("Invalid mode. Use 'linear' or 'circular'.")

    return result.tolist()


def library_correlation(x, y, mode="linear"):
    """
    Computes correlation using numpy built-in correlation.
    mode: 'linear' uses 'full'; 'circular' uses FFT
    """
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