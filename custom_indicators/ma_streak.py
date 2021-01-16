import numpy as np
import tulipy as ti
from helpers import same_length
from typing import Union
from jesse.helpers import get_candle_source


def ma_streak(candles: np.ndarray,
              ma_period: int = 4,
              source_type="close",
              sequential=False) -> Union[float, np.ndarray]:
    """
    MA Streak
    Port of: https://www.tradingview.com/script/Yq1z7cIv-MA-Streak-Can-Show-When-a-Run-Is-Getting-Long-in-the-Tooth/
    :param candles: np.ndarray
    :param ma_period: int - default: 4
    :param source_type: str - default: "close"
    :param sequential: bool - default: False
    :return: Union[float, np.ndarray]
    """
    if not sequential and len(candles) > 240:
        candles = candles[-240:]

    src = get_candle_source(candles, source_type=source_type)
    
    avgval = ti.zlema(np.ascontiguousarray(src), period=ma_period)

    arr = np.diff(avgval)
    pos = np.clip(arr, 0, 1).astype(bool).cumsum()
    neg = np.clip(arr, -1, 0).astype(bool).cumsum()
    streak = np.where(arr >= 0, pos - np.maximum.accumulate(np.where(arr <= 0, pos, 0)),
                      -neg + np.maximum.accumulate(np.where(arr >= 0, neg, 0)))

    res = same_length(src, streak)

    if sequential:
        return res
    else:
        return res[-1]
