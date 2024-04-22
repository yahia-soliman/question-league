import os

os.environ["DB_NAME"] = ":memory:"
os.environ["DB_ENGINE"] = "sqlite"
os.environ["ENV_TYPE"] = "test"
