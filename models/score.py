#!/usr/bin/python3
"""ORM wrapper for user scoring in categories relationship"""
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, validates

from models import Base
from models.engine.sql import session


class Score(Base):
    """The scores of the users in each category"""

    __tablename__ = "user_scores"
    score: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), primary_key=True
    )

    @validates("score")
    def set_score(self, _, value):
        """increment the score"""
        if not self.score:
            return value
        return self.score + value

    def save(self):
        """save changes to the database"""
        session.merge(self)
        session.commit()
        session.close()

    @property
    def total_score(self):
        """get the latest score from the database"""
        filters = []
        filters.append(Score.user_id == self.user_id)
        filters.append(Score.category_id == self.category_id)
        sc = session.query(Score).filter(*filters).first()
        return sc.score if sc else self.score

    @classmethod
    def all(cls):
        """Get all scores"""
        return session.query(cls).all()

    def to_dict(self):
        """Serialize the score object"""
        obj = self.__dict__.copy()
        obj.pop("_sa_instance_state", 0)
        return obj
