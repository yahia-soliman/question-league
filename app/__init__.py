"""The entry point of the flask application."""

__import__("dotenv").load_dotenv()

from flask import Flask

from app.api.v1 import api_v1
from app.main import pages

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(api_v1)
app.register_blueprint(pages)
