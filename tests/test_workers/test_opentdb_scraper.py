from unittest import mock

from models.category import Category
from models.question import Question
from workers import opentdb_scraper as worker


@mock.patch("requests.get")
def test_get_token(mock_get):
    """Test that the get token function works"""
    mock_get.return_value.json = lambda: {"token": "testtoken"}
    token = worker.get_token()
    assert token == "testtoken"


@mock.patch("requests.get")
def test_get_questions(mock_get):
    """test that the return is always list"""
    mock_get.return_value.ok = True
    mock_get.return_value.json = lambda: {"results": ["a", "b", "c"]}
    res = worker.get_questions()
    assert type(res) is list
    mock_get.return_value.ok = False

    res = worker.get_questions("some_token")
    assert type(res) is list


def test_reformat():
    """ensure that the reformating is compatible with the question Object"""
    formatted = worker.reformat(opentdb_result[0])
    expected = {
        "points": 200,
        "category_id": 9,
        "question": "This trope refers to minor characters that are killed off to show how a monster works.",
        "right_answer": "Red Shirt",
        "answers": sorted(["Minions", "Expendables", "Cannon Fodder", "Red Shirt"]),
    }
    for k, v in formatted.items():
        assert expected[k] == v


def test_store_questions():
    """test that the function stores the questions into the database"""
    Category(name="kaka ala ala53r", id=9)
    all_was = len(Question.all())
    worker.store_questions(opentdb_result)
    all_is = len(Question.all())
    assert all_is == all_was + len(opentdb_result)


opentdb_result = [
    {
        "type": "multiple",
        "difficulty": "medium",
        "question": "This trope refers to minor characters that are killed off to show how a monster works.",
        "correct_answer": "Red Shirt",
        "incorrect_answers": ["Minions", "Expendables", "Cannon Fodder"],
    },
    {
        "type": "boolean",
        "difficulty": "medium",
        "question": "There exists an island named &quot;Java&quot;.",
        "correct_answer": "True",
        "incorrect_answers": ["False"],
    },
    {
        "type": "multiple",
        "difficulty": "medium",
        "question": "What disease crippled President Franklin D. Roosevelt and led him to help the nation find a cure? ",
        "correct_answer": "Polio",
        "incorrect_answers": ["Cancer", "Meningitis", "HIV"],
    },
    {
        "type": "multiple",
        "difficulty": "medium",
        "question": "Which one of these Rammstein songs has two official music videos?",
        "correct_answer": "Du Riechst So Gut",
        "incorrect_answers": ["Du Hast", "Benzin", "Mein Teil"],
    },
    {
        "type": "multiple",
        "difficulty": "medium",
        "question": "Which Batman sidekick is the son of Talia al Ghul?",
        "correct_answer": "Damian Wayne",
        "incorrect_answers": ["Dick Grayson", "Tim Drake", "Jason Todd"],
    },
    {
        "type": "multiple",
        "difficulty": "medium",
        "question": "Which of the following bands is Tom DeLonge not a part of?",
        "correct_answer": "+44",
        "incorrect_answers": ["Box Car Racer", "Blink-182", "Angels &amp; Airwaves"],
    },
    {
        "type": "multiple",
        "difficulty": "medium",
        "question": "What engine did the original &quot;Half-Life&quot; run on?",
        "correct_answer": "GoldSrc",
        "incorrect_answers": ["Source", "Quake", "Unreal"],
    },
    {
        "type": "multiple",
        "difficulty": "easy",
        "question": "Which universe crossover was introduced in the &quot;Sonic the Hedgehog&quot; comic issue #247?",
        "correct_answer": "Mega Man",
        "incorrect_answers": ["Super Mario Brothers", "Alex Kidd", "Super Monkey Ball"],
    },
    {
        "type": "multiple",
        "difficulty": "medium",
        "question": "In Calvin and Hobbes, what is the name of the principal at Calvin&#039;s school?",
        "correct_answer": "Mr. Spittle",
        "incorrect_answers": ["Mr. Boreman", "Mr. Spitling", "Mr. Moe"],
    },
    {
        "type": "multiple",
        "difficulty": "medium",
        "question": "Which 90&#039;s comedy cult classic features cameos appearances from Meat Loaf, Alice Cooper and Chris Farley?",
        "correct_answer": "Wayne&#039;s World",
        "incorrect_answers": [
            "Bill &amp; Ted&#039;s Excellent Adventure",
            "Dumb and Dumber",
            "Austin Powers: International Man of Mystery",
        ],
    },
]
