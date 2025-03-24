import numpy as np
import struct


def save_signal(file_path, signal, signal_type, amplitude, duration):
    try:
        with open(file_path, "wb") as f:
            signal_type_bytes = signal_type.encode("utf-8")
            f.write(struct.pack("I", len(signal_type_bytes)))
            f.write(signal_type_bytes)

            f.write(struct.pack("ff", amplitude, duration))

            np.array(signal, dtype=np.float64).tofile(f)
    except Exception as e:
        print(f"Błąd zapisu pliku: {e}")


def load_signal(file_path):
    try:
        with open(file_path, "rb") as f:
            name_length = struct.unpack("I", f.read(4))[0]
            signal_type = f.read(name_length).decode("utf-8")

            amplitude, duration = struct.unpack("ff", f.read(8))

            signal = np.fromfile(f, dtype=np.float64)

        return signal_type, amplitude, duration, signal
    except Exception as e:
        print(f"Błąd odczytu pliku: {e}")
        return None
