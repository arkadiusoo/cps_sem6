import numpy as np


def uniform_dist_noise(amplitude, start, duration, sample_rate=None):
    noise = []
    user_noise = []
    i = 0
    j = 0
    while i < duration:
        value = 0
        if i > start:
            value = np.random.uniform(-amplitude, amplitude)
        noise.append([value, i])
        if sample_rate is not None:
            i += 1 / (3 * sample_rate)
            j += 1
            if j % 3 == 0:
                user_noise.append([value, i])
                j = 0
        else:
            sample_rate += 1/1000
    return noise, user_noise


def gauss_noise(amplitude, start, duration, sample_rate=None):
    noise = []
    user_noise = []
    i = 0
    j = 0
    while i < duration:
        value = 0
        if i > start:
            value = np.random.normal(0, amplitude)
        if sample_rate is not None:
            i += 1 / (3 * sample_rate)
            j += 1
            if j % 3 == 0:
                user_noise.append([value, i])
                j = 0
        else:
            sample_rate += 1 / 1000
    return noise, user_noise


def sinus(amplitude, period, start, duration, sample_rate=1000):
    sinus = []
    i = 0
    while i < duration:
        sinus.append(amplitude * np.sin(((2 * np.pi) / period) * (i - start)))
    return sinus


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
        if i % (2 * kw) == 0:
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
        if i % (2 * kw) == 0:
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
        if i % (2 * kw) == 0:
            k += 1
        triangle.append(value)
    return triangle, time
