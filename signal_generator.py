import numpy as np


def uniform_dist_noise(amplitude, start, duration, sample_rate=1000):
    time = np.linspace(start, duration, num=sample_rate)
    return np.random.uniform(-amplitude, amplitude, len(time)), time


def gauss_noise(amplitude, start, duration, sample_rate=1000):
    time = np.linspace(start, duration, num=sample_rate)
    return np.random.normal(0, amplitude, len(time)), time


def sinus(amplitude, period, start, duration, sample_rate=1000):
    time = np.linspace(start, duration, num=sample_rate)
    sinus = []
    for i in range(len(time)):
        sinus.append(amplitude * np.sin(((2 * np.pi) / period) * (i - start)))
    return sinus, time


def sinus_abs(amplitude, period, start, duration, sample_rate=1000):
    time = np.linspace(start, duration, num=sample_rate)
    sinus = []
    for i in range(len(time)):
        sinus.append(
            amplitude * abs(np.sin(((2 * np.pi) / period) * (i - start))))
    return sinus, time


def sinus_one_half(amplitude, period, start, duration, sample_rate=1000):
    time = np.linspace(start, duration, num=sample_rate)
    sinus = []
    for i in range(len(time)):
        sinus.append(
            (amplitude * ((np.sin(((2 * np.sin) / period) * (i - start))) +
                          abs((np.sin(
                              ((2 * np.sin) / period) * (i - start)))))) / 2)
    return sinus, time
