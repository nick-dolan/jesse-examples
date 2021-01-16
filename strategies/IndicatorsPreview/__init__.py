from jesse.strategies import Strategy
from datetime import datetime, timezone
import custom_indicators as cta


class IndicatorsPreview(Strategy):
    # Momentum Pinball
    @property
    def mp(self):
        return cta.mp(self.candles[:, 2], roc_period=1, rsi_period=3, sequential=False)

    # MA Streak
    @property
    def ma_streak(self):
        return cta.ma_streak(self.candles, ma_period=5, sequential=False)

    # Moving Average Cross (Market Color)
    @property
    def mac(self):
        return cta.mac(self.candles, 20, 50, sequential=False)

    # Net Price Trend
    @property
    def npt(self):
        return cta.npt(self.candles, period=34, period_ma=5, sequential=False)

    # Zero Lag Keltner Channels
    @property
    def zlkc(self):
        return cta.zlkc(self.candles, period=20, mult=1, sequential=False)

    def should_long(self) -> bool:
        return False

    def should_short(self) -> bool:
        return False

    def should_cancel(self) -> bool:
        return True

    def go_long(self):
        pass

    def go_short(self):
        pass

    def after(self):
        date = datetime.fromtimestamp(int(self.current_candle[0]) / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")

        print("{0}, Momentum Pinball: {1}".format(date, round(self.mp, 2)))
        print("{0}, MA Streak: {1}".format(date, self.ma_streak))
        print("{0}, Moving Average Cross: {1}".format(date, self.mac))
        print("{0}, Net Price Trend: {1}".format(date, round(self.npt, 2)))
        print("{0}, ZLKC: {1} {2} {3}".format(date, self.zlkc.upperband, self.zlkc.middleband, self.zlkc.lowerband))
