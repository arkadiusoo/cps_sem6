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

def reconstruct_zoh(times, values, resolution=100):
    reconstructed = []
    for i in range(len(values) - 1):
        t_start = times[i]
        t_end = times[i+1]
        for j in range(resolution):
            t = t_start + (j / resolution) * (t_end - t_start)
            reconstructed.append([values[i], t])

    reconstructed.append([values[-1], times[-1]])
    return reconstructed

def reconstruct_foh(times, values, resolution=100):
    reconstructed = []
    for i in range(len(values) - 1):
        t_start = times[i]
        t_end = times[i+1]
        for j in range(resolution):
            t = t_start + (j / resolution) * (t_end - t_start)

            y = values[i] + (values[i+1] - values[i]) * (t - t_start) / (t_end - t_start)
            reconstructed.append([y, t])
    reconstructed.append([values[-1], times[-1]])
    return reconstructed

def reconstruct_sinc(times, values, t_range=None, resolution=1000):
    if t_range is None:
        t_range = (min(times), max(times))

    t_interp = np.linspace(t_range[0], t_range[1], resolution)
    y_interp = np.zeros_like(t_interp)

    Ts = times[1] - times[0]
    for n in range(len(times)):
        y_interp += values[n] * np.sinc((t_interp - times[n]) / Ts)

    return list(zip(y_interp.tolist(), t_interp.tolist()))
