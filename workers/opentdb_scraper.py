#!/usr/bin/python3
"""Module to scrape and reformat the question objects from opentdb.com api"""

from datetime import datetime as dt
from threading import Timer

import requests

from models.question import Question

categories = {
    "any": 9,
    "General Knowledge": 9,
    "Entertainment: Books": 10,
    "Entertainment: Film": 11,
    "Entertainment: Music": 12,
    "Entertainment: Musicals &amp; Theatres": 13,
    "Entertainment: Television": 14,
    "Entertainment: Video Games": 15,
    "Entertainment: Board Games": 16,
    "Science &amp; Nature": 17,
    "Science: Computers": 18,
    "Science: Mathematics": 19,
    "Mythology": 20,
    "Sports": 21,
    "Geography": 22,
    "History": 23,
    "Politics": 24,
    "Art": 25,
    "Celebrities": 26,
    "Animals": 27,
    "Vehicles": 28,
    "Entertainment: Comics": 29,
    "Science: Gadgets": 30,
    "Entertainment: Japanese Anime &amp; Manga": 31,
    "Entertainment: Cartoon &amp; Animations": 32,
}


def get_token():
    """get a session token from opentdb"""
    res = requests.get("https://opentdb.com/api_token.php?command=request")
    # this token will ensure no duplicates are requested during the session
    return res.json().get("token")


def get_questions(token=None):
    """get 50 question from the api"""
    params = {"amount": 46}
    if token:
        params["token"] = token
    res = requests.get("https://opentdb.com/api.php", params=params)
    if res.ok:
        return res.json().get("results", [])
    else:
        return []


def reformat(question: dict):
    """reformat a question from opentdb to questionleague foramtting"""
    points = {"hard": 300, "medium": 200, "easy": 100}
    return {
        "question": question["question"],
        "answers": sorted(
            question["incorrect_answers"] + [question["correct_answer"]],
        ),
        "right_answer": question["correct_answer"],
        "points": points[question.get("difficulty", "easy")],
        "category_id": categories[question.get("category", "any")],
    }


def store_questions(questions: list):
    """Store a question league formatted question into the current db storage"""
    for q in questions:
        Question(**reformat(q))
    Question.save()


def work(token=None, interval=30):
    """Do a scraping cycle."""
    print(dt.now().strftime("%d %h %Y - %H:%M:%S "), end="")
    print("[WORKER opentdb] fetching...")
    qs = get_questions(token)
    if len(qs) == 0:
        print(dt.now().strftime("%d %h %Y - %H:%M:%S "), end="")
        print("[WORKER opentdb] exiting... no data found")
        exit(0)
    print(dt.now().strftime("%d %h %Y - %H:%M:%S "), end="")
    print(f"[WORKER opentdb] storing {len(qs)} questions... ", end="")
    store_questions(qs)
    print(f"done.")
    Timer(interval, work, [token, interval]).start()


if __name__ == "__main__":
    import os

    import dotenv

    dotenv.load_dotenv()
    token = os.getenv("WORKER_TOKEN")
    if not token:
        token = get_token()
        dotenv.set_key(".env", "WORKER_TOKEN", token)

    print(dt.now().strftime("%d %h %Y - %H:%M:%S "), end="")
    print("[WORKER opentdb] started...")
    work(token, int(os.getenv("WORKER_INTERVAL", 30)))
