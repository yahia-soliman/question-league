"""The SQLAlchemy instance wrapper"""

from os import getenv

from models.engine import Engine

DB = getenv("DB_NAME", "")
USER = getenv("DB_USER", "")
PASS = getenv("DB_PASS", "")
HOST = getenv("DB_HOST", "")
ENGINE = getenv("DB_ENGINE", "").lower()

DB_URI = {
    "sqlite": f"sqlite:///{DB}",
    "mysql": f"mysql+mysqldb://{USER}:{PASS}@{HOST}/{DB}",
}.get(ENGINE, None)


class SQLEngine(Engine):
    """The SQLAlchemy orm"""

    def __init__(self):
        self.uri = DB_URI
