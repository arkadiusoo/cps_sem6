import numpy as np

def save_signal(file_path, signal):
    signal.astype(np.float64).tofile(file_path)
    print(f"Zapisano sygnał do {file_path}")

def load_signal(file_path):
    signal = np.fromfile(file_path, dtype=np.float64)
    print(f"Wczytano sygnał z {file_path}")
    return signal
