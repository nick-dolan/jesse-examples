from typing import Union
import numpy as np
import talib
import pandas as pd


def zlema(src, period=20, sequential=False) -> Union[float, np.ndarray]:
	"""
	Zero-Lag Exponential Moving Average
	This version of ZLEMA can receive source array with nan inside.

	:param src: np.ndarray
	:param period: int - default: 20
	:param sequential: bool - default=False

	:return: float | np.ndarray
	"""
	if not sequential and len(src) > 240:
		src = src[-240:]

	lag = (period - 1) / 2
	src = pd.Series(src)

	ema = pd.Series(src + (src.diff(lag))).to_numpy()

	res = talib.EMA(ema, timeperiod=period)

	if sequential:
		return res
	else:
		return res[-1]
