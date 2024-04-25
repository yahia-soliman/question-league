#!/usr/bin/python3
"""Module to handle API endpoints related to users"""

from flask import abort, jsonify

from app.api.v1 import api_v1


@api_v1.get("users")
def top_ten():
    """get a list of top 10 users"""
    return "coming soon", 200


@api_v1.post("users/sign-up")
def register():
    """register a new user"""
    return "coming soon", 200


@api_v1.post("users/sign-in")
def login():
    """user sign in"""
    return "coming soon", 200
