"""A worker to backup and restore data"""

import json
import sys
from datetime import datetime

from models.category import Category
from models.question import Question
from models.score import Score
from models.user import User

tables = ["users", "categories", "questions", "user_scores"]
models = [ User, Category, Question, Score]
indices = range(len(tables))


def save_snapshot():
    """Save a snap shot of the data based on the current environment."""
    json_obj = {}
    for i in indices:
        print(f"collecting {tables[i]}..")
        json_obj[tables[i]] = [item.to_dict() for item in models[i].all()]
    path = f"./backup/data-{datetime.now().strftime("%Y%m%d%H%M%S")}.json"
    with open(path, "w") as file:
        json.dump(json_obj, file)
        print(f"done")


def load_snapshot(path):
    """Apply the data on a snapshot to the current environment"""
    json_obj = {}
    with open(path, "r") as file:
        json_obj.update(json.load(file))
    for i in indices:
        print(f"loading {tables[i]}")
        j = 0
        for item in json_obj[tables[i]]:
            print(j, end="\r")
            j += 1
            models[i](**item).save()
        print(f"done\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        load_snapshot(sys.argv[1])
    else:
        save_snapshot()
