"""Test the scoring system repsesented in the Score class"""

import pytest

from models.question import Question


@pytest.mark.parametrize(
    "attr",
    [
        "question",
        "points",
        "answers",
        "right_answer",
        "total_tries",
        "right_tries",
        "category_id",
    ],
)
def test_attributes(attr):
    """Test that every initialized object hasd id, creation, updation date"""
    assert hasattr(Question, attr)


def test_answer():
    """test the qustion.answer method"""
    q = Question(
        question="are you ok?",
        answers=["yes", "no", "maybe", "idk"],
        points=200,
        category_id=1,
        right_answer="yes",
    )
    q.save()
    q.answer("wrong")
    assert q.total_tries == 1
    assert q.right_tries == 0
    q.answer("no")
    assert q.total_tries == 2
    assert q.right_tries == 0
    q.answer("yes")
    assert q.total_tries == 3
    assert q.right_tries == 1
