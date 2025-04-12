def perform_signal_operation(signal1, signal2, operation):
    min_len = min(len(signal1), len(signal2))
    sig1 = signal1[:min_len]
    sig2 = signal2[:min_len]

    result = []
    for (y1, t1), (y2, t2) in zip(sig1, sig2):
        if operation == "add":
            result.append([y1 + y2, t1])
        elif operation == "sub":
            result.append([y1 - y2, t1])
        elif operation == "mul":
            result.append([y1 * y2, t1])
        elif operation == "div":
            result.append([y1 / y2 if y2 != 0 else 0, t1])

    return result
