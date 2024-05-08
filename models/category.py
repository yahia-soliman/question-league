#!/usr/bin/python3
"""ORM wrapper for category objects"""
from typing import List

from sqlalchemy import String, func, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base, BaseModel
from models.engine.sql import session
from models.question import Question


class Category(BaseModel, Base):
    """Mapped class for the categories table"""

    __tablename__ = "categories"
    name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    questions: Mapped[List["Question"]] = relationship()
    total_tries: Mapped[int] = mapped_column(default=0)
    right_tries: Mapped[int] = mapped_column(default=0)

    @property
    def total_questions(self):
        q = session.query(func.count(Question.id)).filter(
            Question.category_id == self.id
        )
        return q.scalar()
