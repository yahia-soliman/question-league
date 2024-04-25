"""Test the scoring system repsesented in the Score class"""

import random

import pytest

from models.category import Category
from models.score import Score
from models.user import User

User(username="kokofoko", password="nono", id=122)
Category(name="koka lola", id=212)


@pytest.mark.parametrize("attr", ["user_id", "category_id", "score"])
def test_attributes(attr):
    """Test that every initialized object hasd id, creation, updation date"""
    assert hasattr(Score, attr)


def test_first():
    """if the user have no score i a category a new score object is set"""
    User(username=f"{random.randint(100, 99999)}", password="nono", id=121)
    sc = Score(user_id=121, category_id=212, score=100)
    assert sc.score == 100


@pytest.mark.parametrize("total", [100, 200, 300, 400])
def test_exits(total):
    """user have an old score in category, the score must be incremented"""
    sc = Score(user_id=122, category_id=212, score=100)
    sc.save()
    assert sc.total_score == total
