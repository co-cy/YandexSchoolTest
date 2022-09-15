from pyliteconf import Config as _Config
from os import getenv


class FastApiConfig(_Config):
    """
    Класс с описанием конфигурации FastApi
    """
    pass


class SQLAlchemyConfig(_Config):
    """
    Класс с описанием конфигурации для SQLAlchemy
    """

    _drivers = getenv("DB_DRIVER")
    _user = getenv("DB_USER")
    _password = getenv("DB_PASSWORD")
    _db = getenv("DB_URL")

    url = f"{_drivers}://{_user}:{_password}@{_db}"
