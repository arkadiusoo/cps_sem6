import numpy as np

def dft_from_definition(x, duration):
    """
    Perform Discrete Fourier Transform (DFT) of a signal based on its definition.

    Args:
    - x (list or np.array): Input signal in the time domain.
    - duration (float): Duration of the signal.

    Returns:
    - freq_domain (np.array): Signal in the frequency domain (complex values).
    - freq_axis (np.array): Frequency axis for plotting.
    """
    N = len(x)
    sampling_rate = N / duration
    # Calculate the frequency axis - d - gap between probes, this is X(m) in equation
    freq_axis = np.fft.fftfreq(N, d=1/sampling_rate)

    # Compute the DFT using the formula
    X = np.zeros(N, dtype=complex)  # Initialize an array of complex numbers
    # m - index in frequency domain
    for m in range(N):
        sum_result = 0
        # n - index in time domain
        for n in range(N):
            # Compute the DFT based on the formula: X(m) = sum(x(n) * e^(-j * 2*pi * m * n / N))
            a = x[n]
            sum_result += x[n][1] * np.exp(-1j * 2 * np.pi * m * n / N)
        X[m] = sum_result / N  # Normalize the DFT result

    # Return the frequency domain and frequency axis
    return X, freq_axis

def fft_from_definition(x, duration):
    return 0

def fft_walsh_hadamard_from_definition(x, duration):
    return 0

def fft_walsh_hadamard(x, duration):
    return 0