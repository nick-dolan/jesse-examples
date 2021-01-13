from jesse.strategies import Strategy
from datetime import datetime, timezone
import jesse.indicators as ta
from finta import TA
import pandas as pd


# Examples of how to use FinTA's indicators
class FintaExamples(Strategy):
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

    @property
    def sma(self):
        atr = ta.sma(candles=self.candles, period=100, sequential=True)
        return atr

    @property
    def finta_data_frame(self):
        return pd.DataFrame(data=self.candles, columns=["date", "open", "close", "high", "low", "volume"])

    @property
    def finta_sma(self):
        return TA.SMA(self.finta_data_frame, 100).to_numpy()

    @property
    def finta_vwap(self):
        return TA.VWAP(self.finta_data_frame).to_numpy()

    @property
    def finta_basp(self):
        return TA.BASP(self.finta_data_frame, period=40).to_numpy()

    def after(self):
        date = datetime.fromtimestamp(int(self.current_candle[0]) / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")

        print("{0}, Finta SMA: {1}".format(date, self.finta_sma[-1]))
        print("{0}, Finta VWAP: {1}".format(date, self.finta_vwap[-1]))
        print("{0}, Finta BASP: {1}".format(date, self.finta_basp[-1]))
