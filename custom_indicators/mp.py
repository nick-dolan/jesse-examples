import numpy as np
import talib
from typing import Union


def mp(src: np.ndarray,
       roc_period: int = 1,
       rsi_period: int = 3,
       sequential=False) -> Union[float, np.ndarray]:
    """
    Momentum Pinball
    Port of: https://ru.tradingview.com/script/X9zMa5Fn-Momentum-Pinball/

    :param src: np.ndarray
    :param roc_period: int - default: 1
    :param rsi_period: int - default: 3
    :param sequential: bool - default: False
    :return: Union[float, np.ndarray]
    """
    if not sequential and len(src) > 240:
        src = src[-240:]

    roc = talib.ROC(src, timeperiod=roc_period)
    res = talib.RSI(roc, timeperiod=rsi_period)

    if sequential:
        return res
    else:
        return res[-1]
