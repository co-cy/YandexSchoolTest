from dateutil.parser import isoparse
from datetime import datetime


def datetime_is_correct(string: str) -> datetime | None:
    try:
        return isoparse(string)
    except ValueError:
        return None
