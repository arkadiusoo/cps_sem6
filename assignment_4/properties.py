# discrete
def mean_value_discreate(start, end, probes):
    value = 0
    for probe in probes:
        value += probe[0]
    return value / len(probes)


def absolute_mean_value_discreate(start, end, probes):
    value = 0
    for probe in probes:
        value += abs(probe[0])
    return value / len(probes)


def mean_power_discreate(start, end, probes):
    value = 0
    for probe in probes:
        value += probe[0] ** 2
    return value / len(probes)


def variation_discreate(start, end, probes):
    mean = mean_value_discreate(start, end, probes)
    value = 0
    for probe in probes:
        value += (probe[0] - mean) ** 2
    return value / len(probes)


def effective_value_discreate(start, end, probes):
    return mean_power_discreate(start, end, probes) ** 0.5


# continues properties
def mean_value_continues(start, end, probes):
    value = 0
    delta_t = (end - start) / (len(probes) - 1)
    for i in range(1, len(probes)):
        value += 0.5 * (probes[i][0] + probes[i - 1][0])
    return (value * delta_t) / (end - start)


def absolute_mean_value_continues(start, end, probes):
    value = 0
    delta_t = (end - start) / (len(probes) - 1)
    for i in range(1, len(probes)):
        value += abs(0.5 * (probes[i][0] + probes[i - 1][0]))
    return (value * delta_t) / (end - start)


def mean_power_continues(start, end, probes):
    value = 0
    delta_t = (end - start) / (len(probes) - 1)
    for i in range(1, len(probes)):
        avg = 0.5 * (probes[i][0] + probes[i - 1][0])
        value += avg ** 2
    return (value * delta_t) / (end - start)


def variation_continues(start, end, probes):
    mean = mean_value_continues(start, end, probes)
    value = 0
    delta_t = (end - start) / (len(probes) - 1)
    for i in range(1, len(probes)):
        avg = 0.5 * (probes[i][0] + probes[i - 1][0])
        value += (avg - mean) ** 2
    return (value * delta_t) / (end - start)


def effective_value(start, end, probes):
    return mean_power_continues(start, end, probes) ** 0.5