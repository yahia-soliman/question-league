"""The models needed for the application"""

__import__("dotenv").load_dotenv()

from models.engine import sql

Base = sql.Base
BaseModel = sql.BaseModel
sql.reload()
