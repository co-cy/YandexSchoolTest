from datetime import datetime

from MyDisk.config import TimeConfig


def datetime_is_correct(string: str) -> bool:
    is_correct = False

    for time_format in TimeConfig.time_format:
        try:
            datetime.strptime(string, time_format)
            is_correct = True
            break
        except ValueError:
            pass

    return is_correct
