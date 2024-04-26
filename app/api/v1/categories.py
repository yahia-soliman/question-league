#!/usr/bin/python3
"""Module to handle API endpoints related to users"""

from flask import Blueprint

categories = Blueprint("v1_categories", __name__, url_prefix="categories")


@categories.get("")
def get_all():
    """get all categories stats"""
    return "coming soon", 200


@categories.get("<category_id>")
def category_details(category_id):
    """get details about category"""
    return f"coming soon {category_id}", 200
