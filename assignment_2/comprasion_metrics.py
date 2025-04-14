import numpy as np

def compute_mse(original, reconstructed):
    # Mean Squared Error – Średni błąd kwadratowy

    original = np.array(original)
    reconstructed = np.array(reconstructed)
    return np.mean((original - reconstructed) ** 2)


def compute_snr(original, reconstructed):
    # Signal-to-Noise Ratio – Stosunek sygnału do szumu

    original = np.array(original)
    reconstructed = np.array(reconstructed)
    signal_power = np.mean(original ** 2)
    noise_power = np.mean((original - reconstructed) ** 2)
    if noise_power == 0:
        return float("inf")
    return 10 * np.log10(signal_power / noise_power)


def compute_psnr(original, reconstructed):
    # Peak Signal-to-Noise Ratio – Szczytowy stosunek sygnału do szumu

    original = np.array(original)
    reconstructed = np.array(reconstructed)
    max_val = np.max(original)
    mse = compute_mse(original, reconstructed)
    if mse == 0:
        return float("inf")
    return 10 * np.log10((max_val ** 2) / mse)


def compute_md(original, reconstructed):
    # Maximum Difference – Maksymalna różnica

    original = np.array(original)
    reconstructed = np.array(reconstructed)
    return np.max(np.abs(original - reconstructed))
