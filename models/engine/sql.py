"""The SQLAlchemy storage instance wrapper"""

from os import getenv
from uuid import uuid4

from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

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


class Base(DeclarativeBase):
    """SQLAlchemy's Declarative Base"""


class BaseModel:
    """The Model that every model must enhiret from"""

    id: Mapped[str] = mapped_column(String(60), primary_key=True)

    def __init__(self):
        """initialize an instance of the model"""
        self.id = str(uuid4())
        session.add(self)

    @classmethod
    def all(cls):
        """Get all objects of a class, or all"""
        q = session.query(cls)
        return q.all()

    @classmethod
    def save(cls):
        """Commit changes to the database"""
        session.commit()


def reload():
    """initialize the connection to the database"""
    from models.category import Category
    from models.question import Question
    from models.user import User

    Base.metadata.create_all(engine)


engine = create_engine(DB_URI)
session = Session(engine)
