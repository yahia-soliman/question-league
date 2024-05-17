"""The entry point for the project's API"""

from flask import Blueprint, jsonify

from .categories import categories
from .questions import questions
from .users import users

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")
api_v1.register_blueprint(categories)
api_v1.register_blueprint(questions)
api_v1.register_blueprint(users)


@api_v1.route("status")
def status():
    """check the status of the API"""
    return jsonify({"status": "active"}), 200


@api_v1.route("stats")
def stats():
    """get recent stats of the application"""
    raise Exception("Not implemented")
    # return jsonify({"stats": "we are fine"}), 200
