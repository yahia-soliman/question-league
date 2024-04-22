#!/usr/bin/python3
"""ORM wrapper for user objects"""
from models import Base, BaseModel


class User(BaseModel, Base):
    """Mapped class for the users table"""

    __tablename__ = "users"
