import numpy as np

def generate_signal(signal_type, amplitude, duration, sample_rate=1000):
    time = np.linspace(0, duration, num=sample_rate)

    if signal_type == "Szum jednostajny":
        signal = np.random.uniform(-amplitude, amplitude, size=len(time))
    elif signal_type == "Szum gaussowski":
        signal = np.random.normal(0, amplitude, size=len(time))
    elif signal_type == "Sygnał sinusoidalny":
        signal = amplitude * np.sin(2 * np.pi * time)
    elif signal_type == "Sygnał prostokątny":
        signal = amplitude * np.sign(np.sin(2 * np.pi * time))
    elif signal_type == "Sygnał trójkątny":
        signal = amplitude * np.abs(2 * (time % 1) - 1)
    else:
        signal = np.zeros(len(time))

    return signal, time
