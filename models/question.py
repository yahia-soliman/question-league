#!/usr/bin/python3
"""ORM wrapper for question objects"""
from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models import Base, BaseModel


class Question(BaseModel, Base):
    """Mapped class for the questions table"""

    __tablename__ = "questions"
    question: Mapped[str]
    right_answer: Mapped[str]
    points: Mapped[int]
    answers: Mapped[JSON] = mapped_column(JSON)
    total_tries: Mapped[int] = mapped_column(default=0)
    right_tries: Mapped[int] = mapped_column(default=0)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    def answer(self, value):
        """check if a value is the correct answer"""
        self.total_tries += 1
        if self.right_answer == value:
            self.right_tries += 1
            return self.points
