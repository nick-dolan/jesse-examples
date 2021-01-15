import numpy as np
import talib
from typing import Union


def npt(candles: np.ndarray,
        period: int = 34,
        period_ma: int = 5,
        sequential=False) -> Union[float, np.ndarray]:
    """
    Net Price Trend
    Port of: https://www.tradingview.com/script/KHzxPPx0-Indicator-Net-Price-Trend-xQT5/

    :param candles: np.ndarray
    :param period: int - default: 34
    :param period_ma: int - default: 2
    :param sequential: bool - default: False
    :return: Union[float, np.ndarray]
    """
    if not sequential and len(candles) > 240:
        candles = candles[-240:]

    candles_open = candles[:, 1]
    candles_close = candles[:, 2]
    candles_high = candles[:, 3]
    candles_low = candles[:, 4]

    co = candles_close - candles_open
    hl = candles_high - candles_low

    period = period - 1

    highest = np.full_like(hl, np.nan)

    for i in range(period, len(hl)):
        highest[i] = np.max(hl[i - period:i + 1])

    lowest = np.full_like(hl, np.nan)

    for i in range(period, len(hl)):
        lowest[i] = np.min(hl[i - period:i + 1])

    rs = co / (highest - lowest) * 100

    res = talib.WMA(rs, timeperiod=period_ma)

    if sequential:
        return res
    else:
        return res[-1]
