from pyliteconf import Config as _Config


class FastApiConfig(_Config):
    """
    Класс с описанием конфигурации FastApi
    """
    pass


class SQLAlchemyConfig(_Config):
    """
    Класс с описанием конфигурации для SQLAlchemy
    """

    _drivers = "sqlite"
    # _user = ""
    # _password = ""
    _db = "sqlite3.db"

    # {_user}:{_password}@
    url = f"{_drivers}:///{_db}"


class TimeConfig:
    # TODO: Определиться с форматом времени

    time_format: list[str] = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%fZ"
    ]
