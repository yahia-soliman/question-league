#!/usr/bin/python3
"""The route hadler for html pages"""

from flask import Blueprint, abort, redirect, render_template, url_for

from app.socketio import Room

pages = Blueprint("main", __name__)


@pages.route("/")
def home():
    """The landing page of the project"""
    return render_template("home-page.html")


@pages.get("/multiplayer")
def multiplayer():
    """The landing page of the project"""
    return render_template("multiplayer-page.html")


@pages.get("/multiplayer/new")
def new_room():
    """The landing page of the project"""
    room = Room()
    return redirect(url_for("main.join_room", room_id=room.id))


@pages.get("/multiplayer/<room_id>")
def join_room(room_id):
    """Join a multiplayer room"""
    if Room.get(room_id) is None:
        return abort(404)
    return render_template("multiplayer-room-page.html", room_id=room_id)
