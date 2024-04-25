#!/usr/bin/python3
"""Module to handle API endpoints related to users"""

from flask import abort, jsonify

from app.api.v1 import api_v1


@api_v1.get("categories")
def categories():
    """get all categories stats"""
    return "coming soon", 200


@api_v1.get("categories/<category_id>")
def category_details(category_id):
    """get details about category"""
    return f"coming soon {category_id}", 200
