# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Make sure to read the docs about routes if you haven't already:
# https://docs.jesse.trade/docs/routes.html
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from jesse.utils import anchor_timeframe

# Supported timeframes are 1m, 3m, 5m, 15m, 30m, 1h, 2h, 3h, 4h, 6h, 8h, 1D

# trading routes
routes = [
    ('Binance', 'LTC-USDT', '1h', 'BadStreak')
]

# in case your strategy requires extra candles, timeframes, ...
extra_candles = [
    # ('Binance', 'BTC-USDT', anchor_timeframe('4h')),
]
