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
        return cta.ma_streak(self.candles, ma_period=4, sequential=False)

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

    # Zero Lag Bollinger Bands
    @property
    def zlbb(self):
        return cta.zlbb(self.candles, period=20, mult=1.5, sequential=False)

    # Percent Change Channel
    @property
    def pcc(self):
        return cta.pcc(self.candles, period=20, mult=2, sequential=False)

    # Streak ROC
    @property
    def streak_roc(self):
        streak = abs(int(self.ma_streak))
        streak_back_close = self.candles[:, 2][-(streak + 1)]

        return 100 * (self.close - streak_back_close) / streak_back_close

    # MA Streak PCC's signal
    # Port from: https://www.tradingview.com/script/6wwAWXA1-MA-Streak-Change-Channel/
    @property
    def streak_pcc_signal(self):
        if self.streak_roc < self.pcc.lowerband:
            return 'green'
        elif self.streak_roc > self.pcc.upperband:
            return 'red'
        else:
            return 'none'

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
        print("{0}, ZLKC: {1} {2} {3}".format(date, self.zlbb.upperband, self.zlbb.middleband, self.zlbb.lowerband))
        print("{0}, MA Streak PCC's signal: {1}".format(date, self.streak_pcc_signal))
