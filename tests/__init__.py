import os

os.environ["ENV_TYPE"] = "test"

os.environ["DB_NAME"] = ":memory:"
os.environ["DB_ENGINE"] = "sqlite"
