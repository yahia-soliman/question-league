#!/usr/bin/python3
"""Module to handle API endpoints related to users"""

from flask import Blueprint, abort, jsonify

from models.user import User

users = Blueprint("v1_users", __name__, url_prefix="users")


@users.get("")
def top_ten():
    """get a list of top 10 users"""
    return "coming soon", 200


@users.get("/<username>")
def username(username):
    """get user details"""
    user = User.by_username(username)
    if user:
        return jsonify(user.to_dict())
    return abort(404)
