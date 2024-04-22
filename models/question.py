#!/usr/bin/python3
"""ORM wrapper for question objects"""
from models import Base, BaseModel


class Question(BaseModel, Base):
    """Mapped class for the questions table"""

    __tablename__ = "questions"
