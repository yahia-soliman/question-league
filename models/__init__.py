"""The models needed for the application"""

__import__("dotenv").load_dotenv()

from models.engine.sql import SQLEngine

storage = SQLEngine()
storage.reload()
