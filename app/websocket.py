import json
import secrets

from flask import abort
from flask_sock import ConnectionClosed, Server, Sock

sock = Sock()


@sock.route("/multiplayer/<room_id>")
def ws_connect(ws: Server, room_id):
    """socket connection handler, yes everything is here"""
    user_id = "guest:" + secrets.token_hex(3)
    room: Room = Room.get(room_id)
    user = {"user_id": user_id, "socket": ws}
    ws.send(json.dumps({"event": "welcome", "payload": room.info}))
    room.join(user)
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
        Room.__rooms[self.id] = self

    @classmethod
    def get(cls, room_id):
        """check if there is a room with the id `room_id`"""
        return cls.__rooms.get(room_id, None)

    @property
    def info(self):
        """get the current state of the room"""
        d = {
            "users": [],
            "categories": {},
            "ready": 0,
        }
        for user in self.users.values():
            c_id = user.get("category_id")
            d["categories"][c_id] = d["categories"].get(c_id, 0) + 1
            d["ready"] += user.get("ready", 0)
            d["users"].append(user.copy())
            d["users"][-1].pop("socket", 0)
        d["ready"] = d["ready"] > len(d["users"]) // 2
        return d

    def respond(self, message, user_id):
        """handle incoming message events"""
        events = {
            "ready": self.user_ready,
            "category_vote": self.category_vote,
        }
        data = json.loads(message)
        event = events.get(data.get("event"))
        if event:
            payload = data.get("payload", {})
            payload["user_id"] = user_id
            return event(payload)

    def emit(self, event, payload):
        """send the current state of the room to all the party"""
        message = {"event": event, "payload": payload}
        for user in self.users.values():
            user["socket"].send(json.dumps(message))

    def join(self, payload: dict):
        """Add user to a room"""
        self.users[payload["user_id"]] = payload
        self.emit("user_in", {"user_id": payload["user_id"]})

    def exit(self, user_id):
        """Remove a user from a room"""
        if len(self.users) == 1:
            del Room.__rooms[self.id]
        self.users.pop(user_id, 0)
        self.emit("user_out", {"user_id": user_id})

    def user_ready(self, payload: dict):
        """handle answer event"""
        user = self.users.get(payload.get("user_id"))
        if user:
            user["ready"] = not user.get("ready", False)
            self.emit("user_ready", payload.get("user_id"))

    def category_vote(self, payload):
        """handle the voting for categories"""
        user = self.users.get(payload.get("user_id"))
        if user:
            user["category_id"] = payload.get("category_id")
            self.emit("votes", self.info.get("categories"))
