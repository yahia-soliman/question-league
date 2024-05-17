"""The entry point of the flask application."""

__import__("dotenv").load_dotenv()

from os import getenv

import appsignal
from flask import Flask, Response, url_for
from flask_cors import CORS

from app.api.v1 import api_v1
from app.main import pages
from app.main.auth import login_manager
from app.pubsub import publish, subscribe
from app.websocket import sock
from models import close_connection

appsignal.start()
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SECRET_KEY"] = getenv("FLASK_SECRET", "soso")
app.register_blueprint(api_v1)
app.register_blueprint(pages)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
sock.init_app(app)
login_manager.init_app(app)


@app.teardown_request
def close_db(error):
    """Close Storage"""
    close_connection()


@app.route("/ping")
def ping():
    """play ping pong with the server"""
    return Response(subscribe(), mimetype="text/event-stream")


@app.route("/pong")
def pong():
    """send a to clients listening to ping"""
    publish("data: pong\n\n")
    return "", 200
