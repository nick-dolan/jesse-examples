from jesse.strategies import Strategy
from jesse import utils
import jesse.indicators as ta
import custom_indicators as cta
import numpy as np
import tulipy as ti
from datetime import datetime, timezone, timedelta
from helpers import same_length


class Pinball(Strategy):
    def __init__(self):
        super().__init__()
        self.vars['greed'] = None
        self.vars['allow_trade'] = True
        self.vars['prevent_trade_till_date'] = None

    def should_cancel(self) -> bool:
        return False

    @property
    def mp(self):
        return cta.mp(self.candles[:, 2], roc_period=1, rsi_period=3, sequential=False)

    @property
    def mac(self):
        return cta.mac(self.candles, 20, 50, sequential=True)

    @property
    def npt(self):
        return cta.npt(self.candles, period=34, period_ma=5, sequential=False)

    # Relative percent for setting up stop loss and take profit
    @property
    def greed(self):
        tr = ta.trange(candles=self.candles, sequential=True)
        core = tr[np.logical_not(np.isnan(tr))]
        vwma_tr = ti.vwma(np.ascontiguousarray(core), np.ascontiguousarray(self.candles[:, 5]), period=200)
        return (same_length(self.candles[:, 5], vwma_tr) / self.candles[:, 2] * 100 * 2)[-1]

    @property
    def fast_ema(self):
        return ta.ema(self.candles, period=34, source_type="close")

    @property
    def slow_ema(self):
        return ta.ema(self.candles, period=55, source_type="close")

    @property
    def signal_green(self):
        return self.mp < 25 and self.npt < -18

    @property
    def signal_red(self):
        return self.mp > 75 and self.npt > 18

    @property
    def date(self):
        return datetime.fromtimestamp(int(self.current_candle[0]) / 1000, tz=timezone.utc)

    def should_long(self) -> bool:
        return self.mac[-1] == 1 and self.signal_green and self.fast_ema > self.slow_ema and self.vars['allow_trade']

    def should_short(self) -> bool:
        return self.mac[-1] == -1 and self.signal_red and self.fast_ema < self.slow_ema and self.vars['allow_trade']

    def go_long(self):
        qty = utils.size_to_qty(self.capital * 0.1, self.price, fee_rate=self.fee_rate)
        self.buy = qty, self.price
        self.vars['greed'] = self.greed
        self.take_profit = qty * 0.33, self.price + (self.price * self.greed * 0.4 / 100)

    def go_short(self):
        qty = utils.size_to_qty(self.capital * 0.1, self.price, fee_rate=self.fee_rate)
        self.sell = qty, self.price
        self.vars['greed'] = self.greed
        self.take_profit = qty * 0.33, self.price - (self.price * self.greed * 0.4 / 100)

    def update_position(self):
        if self.is_long:
            if self.close > self.average_entry_price + (self.average_entry_price * self.vars['greed'] / 100):
                self.liquidate()
            elif self.close < self.average_entry_price - (self.average_entry_price * self.vars['greed'] / 100):
                self.liquidate()
            elif self.signal_red:
                self.liquidate()

        if self.is_short:
            if self.close < self.average_entry_price - (self.average_entry_price * self.vars['greed'] / 100):
                self.liquidate()
            elif self.close > self.average_entry_price + (self.average_entry_price * self.vars['greed'] / 100):
                self.liquidate()
            elif self.signal_green:
                self.liquidate()

    def on_stop_loss(self, order):
        self.vars['allow_trade'] = False
        self.vars['prevent_trade_till_date'] = self.date + timedelta(days=3)

    def before(self):
        if self.date == self.vars['prevent_trade_till_date'] or self.mac[-2] != self.mac[-1]:
            self.vars['allow_trade'] = True
