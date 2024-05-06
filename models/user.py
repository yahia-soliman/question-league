#!/usr/bin/python3
"""ORM wrapper for user objects"""
import re
from typing import List

import bcrypt
from flask_login import UserMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from models import Base, BaseModel
from models.engine.sql import session
from models.question import Question
from models.score import Score


class User(BaseModel, Base, UserMixin):
    """Mapped class for the users table"""

    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(72), nullable=False)
    total_score: Mapped[int] = mapped_column(default=0)
    total_tries: Mapped[int] = mapped_column(default=0)
    right_tries: Mapped[int] = mapped_column(default=0)
    scores: Mapped[List[Score]] = relationship()

    @validates("username")
    def validate_username(self, _, username):
        assert username not in unwanted_names
        assert username_regex.match(username)
        return username

    @validates("password")
    def validate_password(self, _, value):
        """validate and hash the password"""
        assert len(value) > 3
        hashed_pass = bcrypt.hashpw(value.encode(), bcrypt.gensalt())
        return hashed_pass.decode()

    @classmethod
    def by_username(cls, username):
        """find one instance in the database by its id"""
        q = session.query(cls).filter(cls.username == username)
        return q.first()

    def to_dict(self):
        """turn the object into a JSON compatible dict"""
        d = super().to_dict()
        d.pop("password")
        return d

    def check_password(self, password: str):
        return bcrypt.checkpw(password.encode(), self.password.encode())

    def answer(self, q: Question, value: str):
        """check if a value is the correct answer"""
        self.total_tries += 1
        reward = q.answer(value)
        if reward:
            self.total_score += reward
            self.right_tries += 1
            Score(user_id=self.id, category_id=q.category_id, score=reward)
            return reward


unwanted_names = []
username_regex = re.compile(
    r"""
    ^                       # beginning of string
    (?!_$)                  # no only _
    [a-zA-Z0-9_]{2,20}      # allowed characters, len from 2 to 32
    $                       # end of string
    """,
    re.X,
)

with open("unwanted_usernames.txt", "r") as f:
    unwanted_names.extend(f.read().split("\n"))
