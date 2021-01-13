import numpy as np
import talib
from jesse import utils
import pandas as pd
from typing import Union


def mac(candles: np.ndarray,
        fast_interval: int = 20,
        slow_interval: int = 50,
        sequential=False) -> Union[float, np.ndarray]:
    """
    Moving Average Cross
    Port of: https://www.tradingview.com/script/PcWAuplI-Moving-Average-Cross/

    :param candles: np.ndarray
    :param fast_interval: int - default: 20
    :param slow_interval: int - default: 50
    :param sequential: bool - default: False
    :return: Union[float, np.ndarray]

    Output: 1: yellow market, -1: red market
    """
    if not sequential and len(candles) > 240:
        candles = candles[-240:]

    candles_high = candles[:, 3]
    candles_low = candles[:, 4]

    # Fast MAs
    upper_fast = talib.EMA(candles_high, timeperiod=fast_interval)
    lower_fast = talib.EMA(candles_low, timeperiod=fast_interval)

    # Slow MAs
    upper_slow = talib.EMA(candles_high, timeperiod=slow_interval)
    lower_slow = talib.EMA(candles_low, timeperiod=slow_interval)

    # Crosses
    crosses_lf_us = utils.crossed(lower_fast, upper_slow, direction=None, sequential=True)
    crosses_uf_ls = utils.crossed(upper_fast, lower_slow, direction=None, sequential=True)

    dir_1 = np.where(crosses_lf_us, 1, np.nan)
    dir_2 = np.where(crosses_uf_ls, -1, np.nan)

    dir = np.where(dir_1 == 1, dir_1, np.nan)
    dir = np.where(dir_2 == -1, dir_2, dir_1)

    res = pd.Series(dir).fillna(method="ffill").to_numpy()

    if sequential:
        return res
    else:
        return res[-1]
