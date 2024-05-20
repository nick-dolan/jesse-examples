from time import strftime, gmtime
from datetime import datetime
import jesse.helpers as jh


def format_minutes(minutes: int) -> str:
    return strftime("%H:%M", gmtime(minutes * 60))


def get_bigger_time_anchor(
        current_date: datetime,
        shorter_timeframe: str,
        longer_timeframe: str) -> bool:
    day_in_minutes = 1440
    shorter_timeframe_in_minutes = jh.timeframe_to_one_minutes(shorter_timeframe)
    bigger_timeframe_in_minutes = jh.timeframe_to_one_minutes(longer_timeframe)
    timeframes_per_day_count = int(day_in_minutes / bigger_timeframe_in_minutes)

    dates = [
        format_minutes(bigger_timeframe_in_minutes * t - shorter_timeframe_in_minutes)
        for t in range(1, timeframes_per_day_count + 1)
    ]

    return current_date.strftime("%H:%M") in dates
