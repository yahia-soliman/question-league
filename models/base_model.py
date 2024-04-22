"""Supply the Base of the curred databse engine"""

from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from models import storage


class Base(DeclarativeBase):
    """SQLAlchemy's Declarative Base"""


class BaseModel:
    """The Model that every model must enhiret from"""

    id: Mapped[str] = mapped_column(String(60), primary_key=True)

    def __init__(self):
        """initialize an instance of the model"""
        self.id = str(uuid4())
        storage.create(self)
