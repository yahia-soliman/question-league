import json
import secrets

from flask import abort
from flask_sock import ConnectionClosed, Server, Sock

sock = Sock()


@sock.route("/multiplayer/<room_id>")
def ws_connect(ws: Server, room_id):
    """socket connection handler, yes everything is here"""
    user_id = "guest:" + secrets.token_hex(3)
    room = Room.get(room_id)
    user = {"user_id": user_id, "socket": ws}
    room.join(user)
    ws.send(f"hello, your id is {user_id}")
    print(f"[INFO] socket: user <{user_id}> connected to the room <{room_id}>")
    if room is None:
        return abort(404)
    try:
        while True:
            message = ws.receive()
            if message:
                room.respond(message, user_id)
    except ConnectionClosed:
        room.exit(user_id)
        ws.close()


class Room:
    """The multiplayer rooms wrapper"""

    # this could be upgraded to Redis or something
    __rooms = {}

    def __init__(self):
        """create a room"""
        self.id = secrets.token_hex(3)
        self.users = {}
        self.ready = set()
        self.category = None
        Room.__rooms[self.id] = self

    @classmethod
    def get(cls, room_id):
        """check if there is a room with the id `room_id`"""
        return cls.__rooms.get(room_id, None)

    def respond(self, message, user_id):
        """handle incoming message events"""
        events = {
            "ready": self.user_ready,
        }
        data = json.loads(message)
        method = events.get(data.get("event"))
        if method:
            payload = data.get("payload", {})
            payload["user_id"] = user_id
            return method(payload)

    def user_ready(self, payload: dict):
        """handle answer event"""
        id = payload.get("user_id")
        if id:
            user = self.users[id]
            user["ready"] = not user.get("ready", False)
            self.ready.add(id)
            self.emit("user_ready", id)

    def emit(self, event, payload):
        """send the current state of the room to all the party"""
        users = self.users.values()
        message = {"event": event, "payload": payload}
        for user in users:
            user["socket"].send(json.dumps(message))

    def join(self, payload: dict):
        """Add user to a room"""
        self.users[payload["user_id"]] = payload
        self.emit("user_in", {"user_id": payload["user_id"]})

    def exit(self, user_id):
        """Remove a user from a room"""
        self.users.pop(user_id, 0)
        if len(self.users) == 0:
            del Room.__rooms[self.id]
