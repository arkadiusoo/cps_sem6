import numpy as np
import struct


def save_signal(file_path, signal, signal_type, amplitude, duration):
    """ Zapisuje sygnał do pliku binarnego z metadanymi """
    try:
        with open(file_path, "wb") as f:
            # Zapisujemy długość nazwy sygnału i samą nazwę (do odczytu)
            signal_type_bytes = signal_type.encode("utf-8")
            f.write(struct.pack("I", len(signal_type_bytes)))  # Długość nazwy
            f.write(signal_type_bytes)  # Nazwa sygnału

            # Zapisujemy metadane (amplituda i czas trwania)
            f.write(struct.pack("ff", amplitude, duration))

            # Zapisujemy dane sygnału jako float64
            np.array(signal, dtype=np.float64).tofile(f)
    except Exception as e:
        print(f"Błąd zapisu pliku: {e}")


def load_signal(file_path):
    """ Wczytuje sygnał z pliku binarnego """
    try:
        with open(file_path, "rb") as f:
            # Odczytujemy długość nazwy sygnału i samą nazwę
            name_length = struct.unpack("I", f.read(4))[0]
            signal_type = f.read(name_length).decode("utf-8")

            # Odczytujemy amplitudę i czas trwania
            amplitude, duration = struct.unpack("ff", f.read(8))

            # Wczytujemy dane sygnału
            signal = np.fromfile(f, dtype=np.float64)

        return signal_type, amplitude, duration, signal
    except Exception as e:
        print(f"Błąd odczytu pliku: {e}")
        return None
