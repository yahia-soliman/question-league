#!/usr/bin/python3
"""Module to handle API endpoints related to questions"""

from flask import abort, jsonify

from app.api.v1 import api_v1
from models.question import Question


@api_v1.get("questions/random")
def get_question():
    """Get a random question"""
    q = Question.random(category_id=1)
    if q:
        return jsonify(q.to_dict()), 200
    else:
        abort(404)


@api_v1.post("questions/<question_id>/<answer>")
def answer_question(question_id, answer):
    """Answer a question"""
    q = Question().getone(question_id)
    if not q:
        abort(404)
    reward = q.answer(answer)
    if reward:
        return jsonify({"points": reward}), 200
    else:
        return abort(418)
