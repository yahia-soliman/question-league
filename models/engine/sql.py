"""The SQLAlchemy storage instance wrapper"""

from datetime import UTC, datetime
from os import getenv

from sqlalchemy import DateTime, create_engine
from sqlalchemy.orm import (DeclarativeBase, Mapped, Session, mapped_column,
                            scoped_session, sessionmaker)


class Base(DeclarativeBase):
    """SQLAlchemy's Declarative Base"""


class BaseModel:
    """The Model that every model must enhiret from"""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)

    def __init__(self, **kw):
        """initialize an instance of the model"""
        self.__dict__.update(kw)
        self.created_at = datetime.now(UTC)
        self.updated_at = self.created_at
        session.add(self)

    @classmethod
    def all(cls):
        """Get all objects of a class, or all"""
        q = session.query(cls)
        return q.all()

    @classmethod
    def save(cls):
        """Commit changes to the database"""
        try:
            session.commit()
        except:
            session.rollback()
            raise
        session.remove()


def reload():
    """initialize the connection to the database"""
    from models.category import Category
    from models.question import Question
    from models.score import Score
    from models.user import User

    if getenv("ENV_TYPE") == "test":
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if getenv("ENV_TYPE") != "test":
    __import__("dotenv").load_dotenv()

DB = getenv("DB_NAME", "")
USER = getenv("DB_USER", "")
PASS = getenv("DB_PASS", "")
HOST = getenv("DB_HOST", "")
ENGINE = getenv("DB_ENGINE", "").lower()

DB_URI = {
    "sqlite": f"sqlite:///{DB}",
    "mysql": f"mysql+mysqldb://{USER}:{PASS}@{HOST}/{DB}",
}.get(ENGINE, "sqlite:///:memory:")

engine = create_engine(DB_URI)
Session = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
session = scoped_session(Session)
