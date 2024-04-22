#!/usr/bin/python3
"""ORM wrapper for category objects"""
from models.base_model import Base, BaseModel


class Category(BaseModel, Base):
    """Mapped class for the categories table"""

    __tablename__ = "categories"
