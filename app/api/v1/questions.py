#!/usr/bin/python3
"""Module to handle API endpoints related to questions"""

from flask import Blueprint, abort, jsonify, request
from flask_login import current_user

from models.question import Question

questions = Blueprint("v1_qustions", __name__, url_prefix="questions/")


@questions.get("")
def get_question():
    """Get a random question"""
    c_id = request.args.get("c", 0)
    q = Question.random(int(c_id))
    if q:
        return jsonify(q.to_dict(pop=["right_answer"])), 200
    else:
        abort(404)


@questions.get("<id>")
def get_by_id(id):
    """Get a specific question"""
    q = Question().getone(id)
    if not q:
        return abort(404)
    return jsonify(q.to_dict(pop=["right_answer"])), 200


@questions.post("<question_id>")
def answer_question(question_id):
    """Answer a question"""
    q = Question().getone(question_id)
    answer = request.get_data()
    if not q or not answer:
        abort(404)
    if current_user.is_authenticated:
        reward = current_user.answer(q, answer.decode())
    else:
        reward = q.answer(answer.decode())
    return jsonify({"points": reward}), 200
