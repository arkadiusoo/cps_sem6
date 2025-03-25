# discrete
def mean_value_discreate(start, end, probes):
    value = 0
    for probe in probes:
        value += probe[0]
    return value / (end - start + 1)


def absolute_mean_value_discreate(start, end, probes):
    value = 0
    for probe in probes:
        value += abs(probe[0])
    return value / (end - start + 1)


def mean_power_discreate(start, end, probes):
    value = 0
    for probe in probes:
        value += probe[0] ** 2
    return value / (end - start + 1)


def variation_discreate(start, end, probes):
    value = 0
    mean = mean_value_discreate(start, end, probes)
    for probe in probes:
        value += (probe[0] - mean) ** 2
    return value / (end - start + 1)


def effective_value_discreate(start, end, probes):
    return mean_value_discreate(start, end, probes) ** (1 / 2)


# continues properties
def mean_value_continues(start, end, probes):
    value = 0
    for i in range(1, len(probes)):
        value += 0.5 * (probes[i][0] + probes[i - 1][0])
    return value / (end - start)


def absolute_mean_value_continues(start, end, probes):
    value = 0
    for i in range(1, len(probes)):
        value += abs(0.5 * (probes[i][0] + probes[i - 1][0]))
    return value / (end - start)


def mean_power_continues(start, end, probes):
    value = 0
    for i in range(1, len(probes)):
        value += (0.5 * (probes[i][0] + probes[i - 1][0])) ** 2
    return value / (end - start)


def variation_continues(start, end, probes):
    value = 0
    mean = mean_value_continues(start, end, probes)
    for i in range(1, len(probes)):
        value += ((0.5 * (probes[i][0] + probes[i - 1][0])) - mean) ** 2
    return value / (end - start)


def effective_value(start, end, probes):
    return mean_power_continues(start, end, probes) ** (1 / 2)
