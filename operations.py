def add_signals(signal1, signal2):
    added_signal = [signal1[i][0] + signal2[i][0]
                    for i in range(len(signal1))]


def subtract_signals(signal1, signal2):
    subtracted_signal = [signal1[i][0] - signal2[i][0]
                         for i in range(len(signal1))]


def multiply_signals(signal1, signal2):
    multiplied_signal = [signal1[i][0] * signal2[i][0]
                         for i in range(len(signal1))]


def divide_signals(signal1, signal2):
    divided_signal = []
    for i in range(len(signal1)):
        if signal2[i] != 0:
            divided_signal.append(signal1[i] / signal2[i])
        else:
            divided_signal.append(0)
