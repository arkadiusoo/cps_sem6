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
