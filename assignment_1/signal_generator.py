import numpy as np

DEFAULT_CONTINUOUS_RATE = 70
SAMPLE_SKIP_RATIO = 3

def adaptive_rate_decorator(func):
    def wrapper(*args, **kwargs):
        global DEFAULT_CONTINUOUS_RATE

        try:
            if 'duration' in kwargs:
                duration = kwargs['duration']
            else:
                duration = args[3]

            DEFAULT_CONTINUOUS_RATE = max(min(int(1000 / duration), 2000), 70)

        except Exception as e:
            print(f"[WARN] adaptive_rate_decorator failed: {e}")
            DEFAULT_CONTINUOUS_RATE = 70

        return func(*args, **kwargs)
    return wrapper

@adaptive_rate_decorator
def uniform_dist_noise(amplitude, start, duration, sample_rate=None):
    noise = []
    user_noise = []

    time = 0.0
    counter = 0

    while time < duration:
        value = np.random.uniform(-amplitude, amplitude) if time > start else 0
        noise.append([value, time])

        if sample_rate is not None:
            if counter % SAMPLE_SKIP_RATIO == 0:
                user_noise.append([value, time])
            counter += 1
            time += 1 / (sample_rate * SAMPLE_SKIP_RATIO)
        else:
            time += 1 / DEFAULT_CONTINUOUS_RATE

    return noise, user_noise


@adaptive_rate_decorator
def gauss_noise(amplitude, start, duration, sample_rate=None):
    noise = []
    user_noise = []

    time = 0.0
    counter = 0

    while time < duration:
        value = np.random.normal(0, amplitude) if time > start else 0
        noise.append([value, time])

        if sample_rate is not None:
            if counter % SAMPLE_SKIP_RATIO == 0:
                user_noise.append([value, time])
            counter += 1
            time += 1 / (sample_rate * SAMPLE_SKIP_RATIO)
        else:
            time += 1 / DEFAULT_CONTINUOUS_RATE

    return noise, user_noise

@adaptive_rate_decorator
def sinus(amplitude, period, start, duration, sample_rate=None):
    sinus = []
    user_sinus = []

    time = 0.0
    counter = 0

    while time < duration:
        value = amplitude * np.sin(((2 * np.pi) / period) * (time - start)) if time > start else 0
        sinus.append([value, time])

        if sample_rate is not None:
            if counter % SAMPLE_SKIP_RATIO == 0:
                user_sinus.append([value, time])
            counter += 1
            time += 1 / (sample_rate * SAMPLE_SKIP_RATIO)
        else:
            time += 1 / DEFAULT_CONTINUOUS_RATE

    return sinus, user_sinus


@adaptive_rate_decorator
def sinus_abs(amplitude, period, start, duration, sample_rate=None):
    sinus = []
    user_sinus = []

    time = 0.0
    counter = 0

    while time < duration:
        value = amplitude * abs(np.sin(((2 * np.pi) / period) * (time - start))) if time > start else 0
        sinus.append([value, time])

        if sample_rate is not None:
            if counter % SAMPLE_SKIP_RATIO == 0:
                user_sinus.append([value, time])
            counter += 1
            time += 1 / (sample_rate * SAMPLE_SKIP_RATIO)
        else:
            time += 1 / DEFAULT_CONTINUOUS_RATE

    return sinus, user_sinus


@adaptive_rate_decorator
def sinus_one_half(amplitude, period, start, duration, sample_rate=None):
    sinus = []
    user_sinus = []

    time = 0.0
    counter = 0

    while time < duration:
        if time > start:
            base = np.sin(((2 * np.pi) / period) * (time - start))
            value = amplitude * (base + abs(base)) / 2
        else:
            value = 0

        sinus.append([value, time])

        if sample_rate is not None:
            if counter % SAMPLE_SKIP_RATIO == 0:
                user_sinus.append([value, time])
            counter += 1
            time += 1 / (sample_rate * SAMPLE_SKIP_RATIO)
        else:
            time += 1 / DEFAULT_CONTINUOUS_RATE

    return sinus, user_sinus

@adaptive_rate_decorator
def square_classic(amplitude, period, start, duration, kw, sample_rate=None):
    square = []
    user_square = []

    time = 0.0
    counter = 0

    while time < duration:
        value = 0
        if time > start:
            phase = (time - start) % period
            if phase < period * kw:
                value = amplitude

        square.append([value, time])

        if sample_rate is not None:
            if counter % SAMPLE_SKIP_RATIO == 0:
                user_square.append([value, time])
            counter += 1
            time += 1 / (sample_rate * SAMPLE_SKIP_RATIO)
        else:
            time += 1 / DEFAULT_CONTINUOUS_RATE

    return square, user_square

@adaptive_rate_decorator
def square_simetric(amplitude, period, start, duration, kw, sample_rate=None):
    square = []
    user_square = []

    time = 0.0
    counter = 0

    while time < duration:
        value = 0
        if time > start:
            phase = (time - start) % period
            value = -amplitude
            if phase < period * kw:
                value = amplitude

        square.append([value, time])

        if sample_rate is not None:
            if counter % SAMPLE_SKIP_RATIO == 0:
                user_square.append([value, time])
            counter += 1
            time += 1 / (sample_rate * SAMPLE_SKIP_RATIO)
        else:
            time += 1 / DEFAULT_CONTINUOUS_RATE

    return square, user_square

@adaptive_rate_decorator
def triangular(amplitude, period, start, duration, kw, sample_rate=None):
    triangle = []
    user_triangle = []

    time = 0.0
    counter = 0

    while time < duration:
        value = 0
        if time > start:
            phase = (time - start) % period
            if phase < period * kw:
                value = (2 * amplitude / (period * kw)) * phase
            else:
                value = (2 * amplitude / (period * (1 - kw))) * (period - phase)

        triangle.append([value, time])

        if sample_rate is not None:
            if counter % SAMPLE_SKIP_RATIO == 0:
                user_triangle.append([value, time])
            counter += 1
            time += 1 / (sample_rate * SAMPLE_SKIP_RATIO)
        else:
            time += 1 / DEFAULT_CONTINUOUS_RATE

    return triangle, user_triangle

@adaptive_rate_decorator
def jump_signal(amplitude, start, duration, jump_time, sample_rate=None):
    jump = []
    user_jump = []

    time = 0.0
    counter = 0

    while time < duration:
        value = 0
        if time == jump_time:
            value = amplitude / 2
        elif time > jump_time:
            value = amplitude

        jump.append([value, time])

        if sample_rate is not None:
            if counter % SAMPLE_SKIP_RATIO == 0:
                user_jump.append([value, time])
            counter += 1
            time += 1 / (sample_rate * SAMPLE_SKIP_RATIO)
        else:
            time += 1 / DEFAULT_CONTINUOUS_RATE

    return jump, user_jump


# discrete functions
# n1 is the probe id from witch we are counting up till ns

@adaptive_rate_decorator
def one_timer(amplitude, start, ns, duration, sample_rate):
    jump = []

    time = 0.0
    sample_index = 0  # licznik indeksów próbek

    while time < duration:
        value = 0
        if time > start:
            if sample_index == ns:
                value = amplitude
            jump.append([value, time])
            sample_index += 1

        if sample_rate is not None:
            time += 1 / sample_rate
        else:
            time += 1 / DEFAULT_CONTINUOUS_RATE

    return jump, []

@adaptive_rate_decorator
def impulse_noise(amplitude, start, probability, duration, sample_rate):
    noise = []

    time = 0.0

    while time < duration:
        value = 0
        if time > start:
            if np.random.uniform(0, 1) < probability:
                value = amplitude
            noise.append([value, time])

        if sample_rate is not None:
            time += 1 / sample_rate
        else:
            time += 1 / DEFAULT_CONTINUOUS_RATE

    return noise, []
