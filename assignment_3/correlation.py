import numpy as np


def manual_correlation(x, y, mode="linear"):
    """
    Computes correlation R_xy[k] = sum_n x[n] * y[n - k]
    mode: 'linear' or 'circular'
    """

    x = np.array(x)
    y = np.array(y)

    if mode == "circular":
        N = max(len(x), len(y))
        x = np.pad(x, (0, N - len(x)), mode='constant')
        y = np.pad(y, (0, N - len(y)), mode='constant')
        result = np.array([np.sum(np.roll(y, k) * x) for k in range(N)])
    elif mode == "linear":
        result = np.correlate(x, y, mode='full')
    else:
        raise ValueError("Invalid mode. Use 'linear' or 'circular'.")

    return result.tolist()


def library_correlation(x, y, mode="linear"):
    """
    Computes correlation using numpy built-in correlation.
    mode: 'linear' uses 'full'; 'circular' approximated by manual method
    """

    x = np.array(x)
    y = np.array(y)

    if mode == "linear":
        return np.correlate(x, y, mode="full").tolist()
    elif mode == "circular":
        # Circular correlation is not directly supported by np.correlate
        N = max(len(x), len(y))
        x = np.pad(x, (0, N - len(x)), mode='constant')
        y = np.pad(y, (0, N - len(y)), mode='constant')
        return [np.sum(np.roll(y, k) * x) for k in range(N)]
    else:
        raise ValueError("Invalid mode. Use 'linear' or 'circular'.")