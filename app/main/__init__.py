"""The route hadler for html pages"""

from flask import Blueprint, render_template

pages = Blueprint("main", __name__)


@pages.route("/")
def home():
    """The landing page of the project"""
    return render_template("home.html")
