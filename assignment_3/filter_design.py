import numpy as np
from assignment_3.filter_windows import (hanning_window, rectangular_window, get_window_function)

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
    h = np.zeros(M)
    h[m] = (w2 - w1) / np.pi
    k = n - m
    h = np.where(k == 0, h[m], (np.sin(w2 * k) - np.sin(w1 * k)) / (np.pi * k))

    if window_type == 'hanning':
        window = hanning_window(M)
    elif window_type == "recnatgular":
        window = rectangular_window(M)
    else:
        return 0

    return h * window

def design_lowpass_fir_filter(Fs, fc, M, window_type='hanning'):

    if M % 2 == 0:
        raise ValueError("M must be odd")

    wc = 2 * np.pi * fc / Fs
    n = np.arange(M)
    m = M // 2

    h = np.zeros(M)
    h[m] = wc / np.pi
    k = n - m
    h = np.where(k == 0, h[m], np.sin(wc * k) / (np.pi * k))

    window = get_window_function(window_type, M)
    return h * window

def design_highpass_fir_filter(Fs, fc, M, window_type='hanning'):

    h_lp = design_lowpass_fir_filter(Fs, fc, M, window_type)
    delta = np.zeros(M)
    delta[M // 2] = 1
    h_hp = delta - h_lp  # Transformacja dolnoprzepustowego na górnoprzepustowy
    return h_hp

def apply_filter(signal, impulse_response):

    return np.convolve(signal, impulse_response, mode='same')