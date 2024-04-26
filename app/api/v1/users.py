#!/usr/bin/python3
"""Module to handle API endpoints related to users"""

from flask import Blueprint

users = Blueprint("v1_users", __name__, url_prefix="users")


@users.get("")
def top_ten():
    """get a list of top 10 users"""
    return "coming soon", 200


@users.post("sign-up")
def register():
    """register a new user"""
    return "coming soon", 200


@users.post("sign-in")
def login():
    """user sign in"""
    return "coming soon", 200
