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
            i += 1 / 1000
    # print(len(noise), len(user_noise))
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
            noise.append([value, i])
        if sample_rate is not None:
            i += 1 / (3 * sample_rate)
            j += 1
            if j % 3 == 0:
                user_noise.append([value, i])
                j = 0
        else:
            i += 1 / 1000
    # print(len(noise), len(user_noise))
    return noise, user_noise


def sinus(amplitude, period, start, duration, sample_rate=None):
    sinus = []
    user_sinus = []
    i = 0
    j = 0
    while i < duration:
        value = 0
        if i > start:
            value = amplitude * np.sin(((2 * np.pi) / period) * (i - start))
            sinus.append([value, i])
        if sample_rate is not None:
            i += 1 / (3 * sample_rate)
            j += 1
            if j % 3 == 0:
                user_sinus.append([value, i])
                j = 0
        else:
            i += 1 / 1000
    # print(len(sinus), len(user_sinus))
    return sinus, user_sinus


def sinus_abs(amplitude, period, start, duration, sample_rate=None):
    sinus = []
    user_sinus = []
    i = 0
    j = 0
    while i < duration:
        value = 0
        if i > start:
            value = amplitude * abs(np.sin(((2 * np.pi) / period) * (i - start)))
            sinus.append([value, i])
        if sample_rate is not None:
            i += 1 / (3 * sample_rate)
            j += 1
            if j % 3 == 0:
                user_sinus.append([value, i])
                j = 0
        else:
            i += 1 / 1000
    # print(len(sinus), len(user_sinus))
    return sinus, user_sinus


def sinus_one_half(amplitude, period, start, duration, sample_rate=None):
    sinus = []
    user_sinus = []
    i = 0
    j = 0
    while i < duration:
        value = 0
        if i > start:
            value = (amplitude * ((np.sin(((2 * np.pi) / period) * (i - start))) +abs((np.sin(((2 * np.pi) / period) * (i - start)))))) / 2
            sinus.append([value, i])
        if sample_rate is not None:
            i += 1 / (3 * sample_rate)
            j += 1
            if j % 3 == 0:
                user_sinus.append([value, i])
                j = 0
        else:
            i += 1 / 1000
    # print(len(sinus), len(user_sinus))
    return sinus, user_sinus


def square_classic(amplitude, period, start, duration, kw, sample_rate=None):
    square = []
    user_square = []
    i = 0
    j = 0
    k = 0
    while i < duration:
        value = 0
        if i > start:
            if (k * period + start <= i
                    < kw * period + k * period + start):
                value = amplitude
            if i % (2 * kw) == 0:
                k += 1
            square.append([value, i])
        if sample_rate is not None:
            i += 1 / (3 * sample_rate)
            j += 1
            if j % 3 == 0:
                user_square.append([value, i])
                j = 0
        else:
            i += 1 / 1000
    # print(len(square), len(user_square))
    return square, user_square


def square_simetric(amplitude, period, start, duration, kw, sample_rate=None):
    square = []
    user_square = []
    i = 0
    j = 0
    k = 0
    while i < duration:
        value = 0
        if i > start:
            value = -amplitude
            if (k * period + start <= i
                    < kw * period + k * period + start):
                value = amplitude
            if i % (2 * kw) == 0:
                k += 1
            square.append([value, i])
        if sample_rate is not None:
            i += 1 / (3 * sample_rate)
            j += 1
            if j % 3 == 0:
                user_square.append([value, i])
                j = 0
        else:
            i += 1 / 1000
    # print(len(square), len(user_square))
    return square, user_square


def triangular(amplitude, period, start, duration, kw, sample_rate=None):
    triangle = []
    user_triangle = []
    i = 0
    j = 0
    k = 0
    while i < duration:
        value = 0
        if i > start:
            value = (-amplitude / (period * (1 - kw))) * (
                    i - k * period - start) + (amplitude / (1 - kw))
            if (k * period + start <= i
                    < kw * period + k * period + start):
                value = (amplitude / (kw * period)) * (
                        i - (k * period) - start)
            if i % (2 * kw) == 0:
                k += 1
            triangle.append([value, i])
        if sample_rate is not None:
            i += 1 / (3 * sample_rate)
            j += 1
            if j % 3 == 0:
                user_triangle.append([value, i])
                j = 0
        else:
            i += 1 / 1000
    # print(len(triangle), len(user_triangle))
    return triangle, user_triangle


def jump_signal(amplitude, start, duration, jump_time, sample_rate=None):
    jump = []
    user_jump = []
    i = 0
    j = 0
    while i < duration:
        value = 0
        if i > start:
            if i == jump_time:
                value = amplitude / 2
            else:
                value = amplitude

            jump.append([value, i])
        if sample_rate is not None:
            i += 1 / (3 * sample_rate)
            j += 1
            if j % 3 == 0:
                user_jump.append([value, i])
                j = 0
        else:
            i += 1 / 1000
    # print(len(jump), len(user_jump))
    return jump, user_jump


# discrete functions
# n1 is the probe id from witch we are counting up till ns


def one_timer(amplitude, start, ns, duration, sample_rate):
    jump = []
    i = 0
    while i < duration:
        value = 0
        if i > start:
            if i == ns:
                value = amplitude
            jump.append([value, i])
        if sample_rate is not None:
            i += 1 / sample_rate
        else:
            i += 1 / 1000
    # print(len(jump))
    return jump, []


def impulse_noise(amplitude, start, probability, duration, sample_rate):
    noise = []
    i = 0
    while i < duration:
        value = 0
        if i > start:
            random_number = np.random.uniform(0, 1)
            if random_number < probability:
                value = amplitude
            noise.append([value, i])
        if sample_rate is not None:
            i += 1 / sample_rate
        else:
            i += 1 / 1000
    # print("dlugosc",len(noise))
    return noise, []
