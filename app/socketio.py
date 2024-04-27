"""Module to handle everything about multiplayer"""

import secrets

from flask import request
from flask_socketio import SocketIO, emit, rooms

sio = SocketIO()


class Room:
    """The multiplayer rooms wrapper"""

    __rooms = {}

    def __init__(self) -> None:
        """create a room"""
        self.id = secrets.token_hex(3)
        self.users = {}
        Room.__rooms[self.id] = self

    @classmethod
    def get(cls, room_id):
        """check if there is a room with the id `room_id`"""
        return cls.__rooms.get(room_id, None)

    def join(self, user):
        """Add user to a room"""
        self.users[user.id] = user

    def exit(self, user):
        """Remove a user from a room"""
        self.users.pop(user.id, 0)

    def __del__(self):
        """Delete the room"""
        Room.__rooms.pop(self.id)


@sio.on("connect")
def client_enter(**socket):
    """New client connected successfully"""
    sid = getattr(request, "sid", None)
    print(f"a new user connected: {sid}\nto the room: {socket}")
    emit("user_in", sid, broadcast=True)


@sio.on("disconnect")
def client_exit():
    """a client disconnected successfully"""
    sid = getattr(request, "sid", None)
    print(f"user diconnected: {sid}")
    emit("user_out", broadcast=True)


@sio.on_error_default
def error_handler(e):
    print("\n[ERROR]an error occured in socketio")
    print(e)
