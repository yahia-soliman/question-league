"""module for testing the SQL storage engine"""

import os
import sys
from unittest import mock

import pytest


@pytest.mark.parametrize("name", ["test", "fungi", "koko"])
def test_sqlite(name):
    """Correct DB_URI is set for sqlite enviroment"""
    with mock.patch.dict(os.environ, {"DB_ENGINE": "sqlite", "DB_NAME": name}):
        sys.modules.pop("models.engine.sql", "")
        DB_URI = __import__("models.engine.sql").engine.sql.DB_URI
        assert DB_URI == f"sqlite:///{name}"


@mock.patch("models.sql.reload")
def test_mysql(reload):
    """Correct DB_URI is set for mysql enviroment"""
    reload.return_value = 0
    env_d = {
        "DB_ENGINE": "mysql",
        "DB_NAME": "mydb",
        "DB_USER": "me",
        "DB_PASS": "mypass",
        "DB_HOST": "myhost",
    }
    with mock.patch.dict(os.environ, env_d):
        sys.modules.pop("models.engine.sql", "")
        DB_URI = __import__("models.engine.sql").engine.sql.DB_URI

        assert DB_URI == "mysql+mysqldb://me:mypass@myhost/mydb"


@pytest.mark.parametrize("engine", ["mydb", "kokodb", ""])
def test_other(engine):
    """any incorrect engine must refere to an in memory sqlite db"""
    with mock.patch.dict(os.environ, {"DB_ENGINE": engine}):
        sys.modules.pop("models.engine.sql", "")
        DB_URI = __import__("models.engine.sql").engine.sql.DB_URI
        assert DB_URI == "sqlite:///:memory:"
