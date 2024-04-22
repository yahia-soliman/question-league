"""The SQLAlchemy storage instance wrapper"""

from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

DB = getenv("DB_NAME", "")
USER = getenv("DB_USER", "")
PASS = getenv("DB_PASS", "")
HOST = getenv("DB_HOST", "")
ENGINE = getenv("DB_ENGINE", "").lower()

DB_URI = {
    "sqlite": f"sqlite:///{DB}",
    "mysql": f"mysql+mysqldb://{USER}:{PASS}@{HOST}/{DB}",
}.get(ENGINE, "sqlite:///:memory:")


class SQLEngine:
    """The SQLAlchemy CRUD handler"""

    models = []

    def __init__(self):
        """Create a storage instance to interact with the database"""
        self.engine = create_engine(DB_URI, echo=True)

    def reload(self):
        """reload the storage"""
        from models.base_model import Base
        from models.category import Category
        from models.question import Question
        from models.user import User

        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        self.models = [Category, Question, User]

    def all(self, model=None):
        """Get all objects of a class, or all"""
        if model:
            q = self.session.query(model)
            return q.all()
        total = []
        for model in self.models:
            q = self.session.query(model)
            total.extend(q.all())
        return total

    def create(self, obj):
        """Create a new object in the database"""
        self.session.add(obj)

    def save(self):
        """Commit changes to the database"""
        self.session.commit()
