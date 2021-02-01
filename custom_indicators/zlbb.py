import numpy as np
from collections import namedtuple
from jesse.helpers import get_candle_source
import custom_indicators as cta
import talib

ZeroLagBollingerBands = namedtuple('ZeroLagBollingerBands', ['upperband', 'middleband', 'lowerband'])


def zlbb(candles: np.ndarray,
		 period: int = 20,
		 mult: float = 1.5,
		 source_type="hlc3",
		 sequential=False) -> ZeroLagBollingerBands:
	"""
	Zero Lag Bollinger Bands
	This is BB with Zero Lag Moving Average (ZLEMA as base).
	https://www.tradingview.com/scripts/bollingerbands/

	:param candles: np.ndarray
	:param period: int - default: 20
	:param mult: float - default: 1.5
	:param source_type: str - default: "hlc3"
	:param sequential: bool - default=False

	:return: ZeroLagBollingerBands(upperband, middleband, lowerband)
	"""
	if not sequential and len(candles) > 240:
		candles = candles[-240:]

	src = get_candle_source(candles, source_type=source_type)
	basis = cta.zlema(src, period=period, sequential=True)
	dev = mult * talib.STDDEV(src, timeperiod=period, nbdev=1)

	upper = basis + dev
	close = candles[:, 2]
	lower = basis - dev

	if sequential:
		return ZeroLagBollingerBands(upper, close, lower)
	else:
		return ZeroLagBollingerBands(upper[-1], close[-1], lower[-1])
