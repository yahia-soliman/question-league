import secrets

from flask import abort
from flask_sock import Sock

sock = Sock()


@sock.route("/multiplayer/<room_id>")
def ws_connect(ws, room_id):
    """socket connection handler, yes everything is here"""
    user_id = "guest:" + secrets.token_hex(3)
    room = Room.get(room_id)
    user = room.join(user_id)
    if room is None:
        return abort(404)
    try:
        while True:
            data = ws.recieve()
            res = room.handle(data, user_id)
            ws.send(res)
    except Exception as e:
        print(f"[ERROR] websocket: {e}")
        # when the connection is closed
        room.exit(user_id)


class Room:
    """The multiplayer rooms wrapper"""

    # this could be upgraded to Redis or something
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

    def join(self, user_id):
        """Add user to a room"""
        self.users[user_id] = {}
        return self.users[user_id]

    def exit(self, user_id):
        """Remove a user from a room"""
        self.users.pop(user_id, 0)
        if len(self.users) == 0:
            del self

    def __del__(self):
        """Delete the room"""
        Room.__rooms.pop(self.id)
