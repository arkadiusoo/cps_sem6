import numpy as np


def uniform_dist_noise(amplitude, start, duration, sample_rate=1000):
    noise = []
    i = 0
    while i < duration:
        value = 0
        if i > start:
            value = np.random.uniform(-amplitude, amplitude)
        noise.append(value)
        i += 1/sample_rate
    return noise


def gauss_noise(amplitude, start, duration, sample_rate=1000):
    noise = []
    i = 0
    while i < duration:
        value = 0
        if i > start:
            value = np.random.normal(0, amplitude)
        noise.append(value)
        i += 1/sample_rate
    return noise


def sinus(amplitude, period, start, duration, sample_rate=1000):
    time = np.linspace(start, duration, num=sample_rate)
    sinus = []
    for i in time:
        sinus.append(amplitude * np.sin(((2 * np.pi) / period) * (i - start)))
    return sinus, time


def sinus_abs(amplitude, period, start, duration, sample_rate=1000):
    time = np.linspace(start, duration, num=sample_rate)
    sinus = []
    for i in time:
        sinus.append(
            amplitude * abs(np.sin(((2 * np.pi) / period) * (i - start))))
    return sinus, time


def sinus_one_half(amplitude, period, start, duration, sample_rate=1000):
    time = np.linspace(start, duration, num=sample_rate)
    sinus = []
    for i in time:
        sinus.append(
            (amplitude * ((np.sin(((2 * np.sin) / period) * (i - start))) +
                          abs((np.sin(
                              ((2 * np.sin) / period) * (i - start)))))) / 2)
    return sinus, time


def square_classic(amplitude, period, start, duration, kw, sample_rate=1000):
    time = np.linspace(start, duration, num=sample_rate)
    square = []
    k = 0
    for i in time:
        value = 0
        if (k * period + start <= i
                < kw * period + k * period + start):
            value = amplitude
        if i % (2*kw) == 0:
            k += 1
        square.append(value)
    return square, time


def square_simetric(amplitude, period, start, duration, kw, sample_rate=1000):
    time = np.linspace(start, duration, num=sample_rate)
    square = []
    k = 0
    for i in time:
        value = -amplitude
        if (k * period + start <= i
                < kw * period + k * period + start):
            value = amplitude
        if i % (2*kw) == 0:
            k += 1
        square.append(value)
    return square, time


def triangular(amplitude, period, start, duration, kw, sample_rate=1000):
    time = np.linspace(start, duration, num=sample_rate)
    triangle = []
    k = 0
    for i in time:
        value = -amplitude
        if (k * period + start <= i
                < kw * period + k * period + start):
            value = amplitude
        if i % (2*kw) == 0:
            k += 1
        triangle.append(value)
    return triangle, time
