import struct
import numpy as np

def save_signal(file_path, signal_list, sampling_list, sampling_type, parameters):
    try:
        with open(file_path, "wb") as f:
            # --- signal_type
            signal_type_bytes = parameters[0].encode("utf-8")
            f.write(struct.pack("I", len(signal_type_bytes)))
            f.write(signal_type_bytes)

            # --- sampling_type (z parameters[3])
            sampling_type_bytes = parameters[3].encode("utf-8")
            f.write(struct.pack("I", len(sampling_type_bytes)))
            f.write(sampling_type_bytes)

            # --- save 9 numeric parameters (excluding 2 strings)
            numeric_params = [float(x) for x in [parameters[1], parameters[2], parameters[4],
                                                 parameters[5], parameters[6], parameters[7],
                                                 parameters[8], parameters[9], parameters[10]]]
            f.write(struct.pack("9d", *numeric_params))

            # --- signal_list
            f.write(struct.pack("I", len(signal_list)))
            for y, t in signal_list:
                f.write(struct.pack("2d", y, t))

            # --- sampling_list
            f.write(struct.pack("I", len(sampling_list)))
            for y, t in sampling_list:
                f.write(struct.pack("2d", y, t))

    except Exception as e:
        print(f"Błąd zapisu pliku: {e}")



def load_signal(file_path):
    try:
        with open(file_path, "rb") as f:
            # --- signal_type
            name_len = struct.unpack("I", f.read(4))[0]
            signal_type = f.read(name_len).decode("utf-8")

            # --- sampling_type
            sampling_name_len = struct.unpack("I", f.read(4))[0]
            sampling_type = f.read(sampling_name_len).decode("utf-8")

            # --- numeric parameters
            raw_numeric = f.read(8 * 9)
            if len(raw_numeric) < 72:
                raise ValueError("Brakuje danych – plik nie zawiera wszystkich parametrów (oczekiwano 72 bajtów).")
            numeric_values = struct.unpack("9d", raw_numeric)

            # --- signal_list
            signal_len = struct.unpack("I", f.read(4))[0]
            signal_list = [list(struct.unpack("2d", f.read(16))) for _ in range(signal_len)]

            # --- sampling_list
            sampling_len = struct.unpack("I", f.read(4))[0]
            sampling_list = [list(struct.unpack("2d", f.read(16))) for _ in range(sampling_len)]

        # reconstruct parameters list
        parameters = [signal_type, numeric_values[0], numeric_values[1], sampling_type] + list(numeric_values[2:])
        return signal_list, sampling_list, sampling_type, parameters

    except Exception as e:
        print(f"Błąd odczytu pliku: {e}")
        return None, None, None, None
