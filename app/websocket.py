import json
import secrets
from threading import Timer

from flask import abort
from flask_login import current_user
from flask_sock import ConnectionClosed, Server, Sock

from models.question import Question

sock = Sock()


@sock.route("/multiplayer/<room_id>")
def ws_connect(ws: Server, room_id):
    """socket connection handler, yes everything is here"""
    room = Room.get(room_id)
    if room is None:
        return ws.close()
    if current_user.is_authenticated:
        user_id = current_user.username
        user = current_user
    else:
        user_id = secrets.token_hex(3) + " (guest)"
        user = None
    if user_id in room.users:
        return ws.close()
    user = {"user_id": user_id, "socket": ws, "user": user}
    info = room.info
    info["user_id"] = user_id
    ws.send(json.dumps({"event": "welcome", "payload": info}))
    room.join(user)
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
        Room.__rooms[self.id] = self
        self.users = {}
        self.category_id = 0
        self.question = None
        self.timer = Timer(30, self.play)
        self.rank = 0
        self.events = {
            "ready": self.user_ready,
            "category_vote": self.category_vote,
            "guest_name": self.guest_name,
        }

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
            d["users"][-1].pop("user", 0)
        if self.question:
            d["started"] = True
            d["question"] = self.question.to_dict()
        d["ready"] = d["ready"] > len(d["users"]) // 2
        return d

    def respond(self, message, user_id):
        """handle incoming message events"""
        try:
            data = json.loads(message)
        except json.decoder.JSONDecodeError:
            socket = self.users.get(user_id, {}).get("socket")
            if socket:
                socket.send("Only JSON is supported")
            return

        event = self.events.get(data.get("event"))
        if event:
            payload = data.get("payload", {})
            payload["user_id"] = user_id
            event(payload)

    def emit(self, event, payload=None):
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
            self.timer.cancel()
            del Room.__rooms[self.id]
        self.users.pop(user_id, 0)
        self.emit("user_out", user_id)

    def play(self):
        """Start asking questions to the users in the room"""
        self.rank = 0
        self.question = Question.random(self.category_id)
        print(f"playing in room {self.id} from category {type(self.category_id)}")
        if self.question:
            self.emit("question", self.question.to_dict())
            self.timer = Timer(30, self.play)
            self.timer.start()

    def user_answer(self, payload):
        """Check user answers and give them score"""
        user = self.users.get(payload.get("user_id"))
        answer = payload.get("answer")
        if user and answer and self.question:
            self.rank += 1
            scale = 1 + 0.1 * abs(len(self.users) - self.rank)
            if user.get("user"):
                score = user["user"].answer(self.question, answer, scale=scale)
            else:
                score = self.question.answer(answer, scale=scale)
            user["score"] = user.get("score", 0) + score
            self.emit("user_answer", {"user_id": user["user_id"], "score": score})
            self.question.save()

    def user_ready(self, payload: dict):
        """handle start-game votes"""
        user = self.users.get(payload.get("user_id"))
        if user:
            user["ready"] = not user.get("ready", False)
            user = user.copy()
            user.pop("socket", 0)
            user.pop("user", 0)
            self.emit("user_ready", user)
            if self.info["ready"]:
                self.emit("game_start")
                del self.events["ready"]
                self.events["answer"] = self.user_answer
                self.play()

    def guest_name(self, payload):
        """Rename the guest name instead of hex values"""
        user = self.users.get(payload.get("user_id"))
        name = payload.get("name", "")
        if user and 1 < len(name) < 15:
            payload["name"] = user["name"] = name + " (guest)"
            self.emit("guest_name", payload)

    def category_vote(self, payload):
        """handle the voting for categories"""
        user = self.users.get(payload.get("user_id"))
        id = payload.get("category_id")
        if user and id:
            user["category_id"] = int(id)
            categories = self.info["categories"]
            self.emit("votes", categories)
            self.category_id = max(categories, key=categories.get)
