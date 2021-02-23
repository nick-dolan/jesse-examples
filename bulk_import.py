from jesse.config import config
from jesse.services import db
from jesse.modes import import_candles_mode

config['app']['trading_mode'] = 'import-candles'

exchange = 'Binance'
start_date = '2019-01-01'

pairs = ['BTC-USDT', 'LTC-USDT', 'XMR-USDT', 'ETC-USDT']

for pair in pairs:
	import_candles_mode.run(exchange, pair, start_date, skip_confirmation=True)

db.close_connection()
