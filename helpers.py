import numpy as np


def point_slope(x1, y1, x2, y2, x):
    m = (y2 - y1) / (x2 - x1)
    x0 = y1 - (m * x1)
    return m * x + x0


def same_length(bigger, shorter):
    return np.concatenate((np.full((bigger.shape[0] - shorter.shape[0]), np.nan), shorter))


def shift(arr, num, fill_value=np.nan):
    result = np.empty_like(arr)
    if num > 0:
        result[:num] = fill_value
        result[num:] = arr[:-num]
    elif num < 0:
        result[num:] = fill_value
        result[:num] = arr[-num:]
    else:
        result[:] = arr
    return result
