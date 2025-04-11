import numpy as np

def sample_signal(signal_values, time_values, sampling_freq):

    sampling_interval = 1.0 / sampling_freq

    start_time = time_values[0]
    end_time = time_values[-1]
    sampled_times = np.arange(start_time, end_time, sampling_interval)

    sampled_values = np.interp(sampled_times, time_values, signal_values)

    return sampled_times.tolist(), sampled_values.tolist()


def quantize_signal(signal_values, num_levels=256, method="round"):

    signal_values = np.array(signal_values)

    min_val = np.min(signal_values)
    max_val = np.max(signal_values)

    step = (max_val - min_val) / (num_levels - 1)

    if method == "truncate":
        indices = ((signal_values - min_val) // step).astype(int)
    elif method == "round":
        indices = np.round((signal_values - min_val) / step).astype(int)
    else:
        raise ValueError("Unknown quantization method. Use 'truncate' or 'round'.")

    quantized_values = min_val + indices * step
    return quantized_values.tolist()

