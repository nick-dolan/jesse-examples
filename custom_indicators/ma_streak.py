import numpy as np
import tulipy as ti
import pandas as pd
from helpers import same_length
from typing import Union


def ma_streak(src: np.ndarray,
              ma_period: int = 4,
              sequential=False) -> Union[float, np.ndarray]:
    """
    MA Streak
    Port of: https://www.tradingview.com/script/Yq1z7cIv-MA-Streak-Can-Show-When-a-Run-Is-Getting-Long-in-the-Tooth/
    :param src: np.ndarray
    :param ma_period: int - default: 4
    :param sequential: bool - default: False
    :return: Union[float, np.ndarray]
    """
    if not sequential and len(src) > 240:
        src = src[-240:]

    avgval = ti.zlema(np.ascontiguousarray(src), period=ma_period)

    s = pd.Series(avgval)
    sd = s.diff()
    pos = s.groupby(sd.lt(0).cumsum()).cumcount()
    neg = s.groupby(sd.gt(0).cumsum()).cumcount()
    streak = np.where(sd > 0, pos, -neg)[1:]
    streak = same_length(src, streak)

    if sequential:
        return streak
    else:
        return streak[-1]
