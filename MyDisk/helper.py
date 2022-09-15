from dateutil.parser import isoparse
from datetime import datetime


def str_to_datetime(string: str) -> datetime | None:
    try:
        return isoparse(string)
    except ValueError:
        return None
