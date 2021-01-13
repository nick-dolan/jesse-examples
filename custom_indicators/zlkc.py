from collections import namedtuple

import numpy as np
import jesse.indicators as ta
import custom_indicators as cta

from jesse.helpers import get_candle_source


ZeroLagKeltnerChannel = namedtuple('ZeroLagKeltnerChannel', ['upperband', 'middleband', 'lowerband'])


def zlkc(candles: np.ndarray,
         period: int = 20,
         mult: float = 1,
         source_type="hlc3",
         sequential=False) -> ZeroLagKeltnerChannel:
    """
    Zero Lag Keltner Channels
    Based on TradingView: https://www.tradingview.com/script/CTzNAuUH-Zero-Lag-Keltner-Channels/

    :param candles: np.ndarray
    :param period: int - default: 20
    :param mult: int - default: 1
    :param source_type: str - default: "hlc3"
    :param sequential: bool - default=False

    :return: ZeroLagKeltnerChannel(upperband, middleband, lowerband)
    """

    source = get_candle_source(candles, source_type=source_type)
    ma = cta.zlema(source, period=period, sequential=True)

    tr = ta.trange(candles=candles, sequential=True)
    rangema = cta.zlema(tr, period=period, sequential=True)

    upper = ma + rangema * mult
    lower = ma - rangema * mult

    if sequential:
        return ZeroLagKeltnerChannel(upper, ma, lower)
    else:
        return ZeroLagKeltnerChannel(upper[-1], ma[-1], lower[-1])

