from jesse.strategies import Strategy
from datetime import datetime, timezone
from helpers import get_bigger_time_anchor


# First select the routes you need. It can be any combination such as 1m/1h, 15m/1h, 1h/4h and so on.
# Second, in the get_bigger_time_anchor method pass longer timeframe, for example 1h.
# Then you can check if the current candle is 1h close and do your calculations like this: `if self.is_bigger_time_anchor`

class MultiCandles(Strategy):
    @property
    def date(self):
        return datetime.fromtimestamp(
            int(self.current_candle[0]) / 1000, tz=timezone.utc
        )

    @property
    def is_bigger_time_anchor(self):
        return get_bigger_time_anchor(self.date, self.timeframe, "1h")

    def should_long(self) -> bool:
        return False

    def go_long(self):
        pass

    def should_short(self) -> bool:
        return False

    def go_short(self):
        pass

    def should_cancel_entry(self) -> bool:
        return True

    def after(self):
        date = self.date.strftime("%Y-%m-%d %H:%M")

        # No matter which lower timeframe we are using, we will always print the close of the bigger timeframe
        if self.is_bigger_time_anchor:
            print(f"{date} CLOSE: {self.price}")