from typing import Union
import numpy as np
import tulipy as ti
from helpers import same_length


def zlema(src, period=20, sequential=False) -> Union[float, np.ndarray]:
    """
    Zero-Lag Exponential Moving Average
    The custom version of ZLEMA can receive a source array with nan inside.

    :param src: np.ndarray
    :param period: int - default: 20
    :param sequential: bool - default=False

    :return: float | np.ndarray
    """
    if not sequential and len(src) > 240:
        src = src[-240:]

    source = src[np.logical_not(np.isnan(src))]  # Remove nan
    res = ti.zlema(np.ascontiguousarray(source), period=period)

    if sequential:
        return same_length(src, np.concatenate((np.full((source.shape[0] - res.shape[0]), np.nan), res), axis=0))
    else:
        return res[-1]
