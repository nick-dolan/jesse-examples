from collections import namedtuple
import numpy as np
import custom_indicators as cta
from helpers import shift

PercentChangeChannel = namedtuple('PercentChangeChannel', ['upperband', 'middleband', 'lowerband'])


def pcc(candles: np.ndarray,
		period: int = 20,
		mult: int = 2,
		sequential=False) -> PercentChangeChannel:
	"""
	Percent Change Channel
	PCC is like KC unless it uses percentage changes in price to set channel distance.
	https://www.tradingview.com/script/6wwAWXA1-MA-Streak-Change-Channel/

	:param candles: np.ndarray
	:param period: int - default: 20
	:param mult: float - default: 2
	:param sequential: bool - default=False

	:return: PercentChangeChannel(upperband, middleband, lowerband)
	"""
	if not sequential and len(candles) > 240:
		candles = candles[-240:]

	close = candles[:, 2]
	previous_close = shift(close, 1, np.nan)
	low = candles[:, 4]
	high = candles[:, 3]

	close_change = (close - previous_close) / previous_close * 100
	high_change = (high - close) / close * 100
	low_change = (low - close) / close * 100

	mid = cta.zlema(close_change, period, sequential=True)
	rangema = cta.zlema(high_change - low_change, period, sequential=True)

	upper = mid + rangema * mult
	lower = mid - rangema * mult

	if sequential:
		return PercentChangeChannel(upper, rangema, lower)
	else:
		return PercentChangeChannel(upper[-1], rangema[-1], lower[-1])
