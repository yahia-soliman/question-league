#!/usr/bin/python3
"""Module to handle API endpoints related to questions"""

from flask import Blueprint, abort, jsonify

from models.question import Question

questions = Blueprint("v1_qustions", __name__, url_prefix="questions/")


@questions.get("")
def get_question():
    """Get a random question"""
    q = Question.random()
    if q:
        return jsonify(q.to_dict()), 200
    else:
        abort(404)


@questions.get("<id>")
def get_by_id(id):
    """Get a random question"""
    q = Question().getone(id)
    if not q:
        return abort(404)
    return jsonify(q.to_dict()), 200


@questions.post("<question_id>/<answer>")
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
