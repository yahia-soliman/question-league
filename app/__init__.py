"""The entry point of the flask application."""

from flask import Flask

from app.api.v1 import api_v1

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(api_v1)


@app.route("/hello")
def hello():
    return "Hello, World!"
