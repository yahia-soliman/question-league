#!/usr/bin/python3
"""ORM wrapper for question objects"""
from sqlalchemy import JSON, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from models import Base, BaseModel
from models.engine.sql import session


class Question(BaseModel, Base):
    """Mapped class for the questions table"""

    __tablename__ = "questions"
    question: Mapped[str] = mapped_column(String(512))
    right_answer: Mapped[str] = mapped_column(String(128))
    points: Mapped[int]
    answers: Mapped[list] = mapped_column(JSON)
    total_tries: Mapped[int] = mapped_column(default=0)
    right_tries: Mapped[int] = mapped_column(default=0)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    def answer(self, value):
        """check if a value is the correct answer"""
        self.total_tries += 1
        if self.right_answer == value:
            self.right_tries += 1
            return self.points

    @classmethod
    def random(cls, category_id=None):
        """get a random question."""
        q = session.query(Question)
        if category_id:
            q = q.filter(Question.category_id == category_id)
        q = q.order_by(func.random())
        return q.first()
