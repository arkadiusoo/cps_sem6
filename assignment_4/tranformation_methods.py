import numpy as np

def dft_from_definition(x, duration, example_signal=False):
    """
    Perform Discrete Fourier Transform (DFT) of a signal based on its definition.

    Args:
    - x (list or np.array): Input signal in the time domain.
    - duration (float): Duration of the signal.

    Returns:
    - freq_domain (np.array): Signal in the frequency domain (complex values).
    - freq_axis (np.array): Frequency axis for plotting.
    """
    if example_signal:

        x = [
        [0, 0],
        [0, 1.74831568647798],
        [0, 3.38589080774217],
        [0, 4.8128711636485],
        [0, 5.94974746830583],
        [0, 6.7441668186291],
        [0, 7.17426350876555],
        [0, 7.2481803951877],
        [0, 7],
        [0, 6.48281353045752],
        [0, 5.76004994639246],
        [0, 4.89640775360653],
        [0, 3.94974746830583],
        [0, 2.96511209862592],
        [0, 1.97167724536908],
        [0, 0.98294882174781],
        [0, 6.12323399573676E-16],
        [0, -0.982948821747808],
        [0, -1.97167724536908],
        [0, -2.96511209862592],
        [0, -3.94974746830583],
        [0, -4.89640775360653],
        [0, -5.76004994639245],
        [0, -6.48281353045752],
        [0, -7],
        [0, -7.2481803951877],
        [0, -7.17426350876555],
        [0, -6.7441668186291],
        [0, -5.94974746830583],
        [0, -4.8128711636485],
        [0, -3.38589080774218],
        [0, -1.74831568647799],
        [0, -2.20436423846523E-15],
        [0, 1.74831568647798],
        [0, 3.38589080774217],
        [0, 4.81287116364849],
        [0, 5.94974746830583],
        [0, 6.7441668186291],
        [0, 7.17426350876555],
        [0, 7.2481803951877],
        [0, 7],
        [0, 6.48281353045752],
        [0, 5.76004994639246],
        [0, 4.89640775360653],
        [0, 3.94974746830583],
        [0, 2.96511209862592],
        [0, 1.97167724536908],
        [0, 0.982948821747806],
        [0, 1.83697019872102E-15],
        [0, -0.982948821747803],
        [0, -1.97167724536908],
        [0, -2.96511209862592],
        [0, -3.94974746830583],
        [0, -4.89640775360652],
        [0, -5.76004994639245],
        [0, -6.48281353045752],
        [0, -6.99999999999999],
        [0, -7.2481803951877],
        [0, -7.17426350876555],
        [0, -6.7441668186291],
        [0, -5.94974746830583],
        [0, -4.8128711636485],
        [0, -3.38589080774218],
        [0, -1.74831568647798],
        [0, -4.40872847693047E-15],
        [0, 1.74831568647797],
        [0, 3.38589080774217],
        [0, 4.81287116364849],
        [0, 5.94974746830583],
        [0, 6.7441668186291],
        [0, 7.17426350876555],
        [0, 7.2481803951877],
        [0, 7],
        [0, 6.48281353045752],
        [0, 5.76004994639246],
        [0, 4.89640775360653],
        [0, 3.94974746830584],
        [0, 2.96511209862593],
        [0, 1.97167724536908],
        [0, 0.982948821747807],
        ]
        N = len(x)
        sampling_rate = 16
    else:
        N = len(x)
        sampling_rate = N / duration


    # Calculate the frequency axis - d - gap between probes, this is X(m) in equation
    freq_axis = np.fft.fftfreq(N, d=1/sampling_rate)

    # Compute the DFT using the formula
    X = np.zeros(N, dtype=complex)  # Initialize an array of complex numbers
    for m in range(N):
        sum_result = 0
        # n - index in time domain
        for n in range(N):
            # Compute the DFT based on the formula: X(m) = sum(x(n) * e^(-j * 2*pi * m * n / N))
            sum_result += x[n][1] * np.exp(-1j * 2 * np.pi * m * n / N)
        X[m] = sum_result / N  # Normalize the DFT result

    # Remove negative frequencies by selecting only positive frequencies and their corresponding values
    positive_freq_mask = freq_axis >= 0
    freq_axis = freq_axis[positive_freq_mask]
    X = X[positive_freq_mask]

    # Return the frequency domain and frequency axis
    return X, freq_axis

def fft_from_definition(x, duration):
    return 0

def fft_walsh_hadamard_from_definition(x, duration):
    return 0

def fft_walsh_hadamard(x, duration):
    return 0