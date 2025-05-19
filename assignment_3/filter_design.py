import numpy as np
from assignment_3.filter_windows import hanning_window

def design_bandpass_fir_filter(Fs, f1, f2, M, window_type='hanning'):
    """
    Designs a band-pass FIR filter using window method.
    Fs: Sampling frequency
    f1, f2: Cutoff frequencies (Hz)
    M: Number of filter coefficients (odd)
    window_type: 'hanning' only for now
    """

    if M % 2 == 0:
        raise ValueError("M must be odd")

    # Normalized frequencies
    w1 = 2 * np.pi * f1 / Fs
    w2 = 2 * np.pi * f2 / Fs
    n = np.arange(M)
    m = M // 2

    # Ideal bandpass impulse response
    h = (np.sin(w2 * (n - m)) - np.sin(w1 * (n - m))) / (np.pi * (n - m))
    h[m] = (w2 - w1) / np.pi  # handle division by zero at center

    if window_type == 'hanning':
        window = hanning_window(M)
    else:
        window = np.ones(M)

    return h * window
