#!/usr/bin/python3
"""The route hadler for html pages"""

from flask import Blueprint, abort, redirect, render_template, request, url_for

from app.main.auth import auth
from app.websocket import Room
from models.category import Category
from models.user import User

pages = Blueprint("main", __name__)
pages.register_blueprint(auth)


@pages.route("/")
def home():
    """The landing page of the project"""
    cats = Category.all()
    users = User.top()
    return render_template("home-page.html", categories=cats, users=users)


@pages.route("/play")
def soloplayer():
    """The single player page"""
    cat0 = {"id": 0, "name": "All"}
    cats = [cat0] + sorted(Category.all(), key=lambda c: c.name)
    return render_template("soloplayer-page.html", categories=cats)


@pages.get("/multiplayer")
def multiplayer():
    """The landing page of the project"""
    room_id = request.args.get("roomId")
    if room_id:
        return redirect(url_for("main.join_room", room_id=room_id))
    return render_template("multiplayer-page.html")


@pages.get("/multiplayer/new")
def new_room():
    """Create a new multiplayer room"""
    room = Room()
    return redirect(url_for("main.join_room", room_id=room.id))


@pages.get("/multiplayer/<room_id>")
def join_room(room_id):
    """Join a multiplayer room"""
    room = Room.get(room_id)
    if room is None:
        return abort(404)

    # a fake category to have a voting field for all categories
    cat0 = {"id": 0, "name": "All"}
    categories = [cat0] + sorted(Category.all(), key=lambda c: c.name)
    return render_template(
        "multiplayer-room-page.html", room=room, categories=categories
    )
