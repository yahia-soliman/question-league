import os
from random import randint
from unittest import mock

import pytest

from models.user import User


@pytest.mark.parametrize(
    "attr",
    [
        "id",
        "created_at",
        "updated_at",
        "username",
        "password",
        "total_score",
        "total_tries",
        "right_tries",
    ],
)
@mock.patch("models.engine.sql.session")
def test_attributes(session, attr):
    """Test that every initialized object hasd id, creation, updation date"""
    session.add = print
    obj = User(username=f"user{randint(1000,9999)}", password="password")
    assert hasattr(obj, attr)


@pytest.mark.parametrize("method", ["save", "all", "check_password"])
def test_methods(method):
    """Test that the base class have mandatory methods"""
    assert callable(getattr(User, method))


@pytest.mark.parametrize(
    "user,passwd", [("kokko", "soso"), ("momo", "roro"), ("ali", "aloka")]
)
def test_pass_hash(user, passwd):
    """Test that the users' passwords is hashed"""
    u = User(username=user, password=passwd)
    assert u.password != passwd
    assert len(u.password) == 60


def test_check_password():
    """Test password hashing and checking functionality"""
    u = User(username="testname", password="testpass")
    assert u.check_password("wrong") is False
    assert u.check_password("testpass") is True


@pytest.mark.parametrize(
    "username",
    [
        "",
        " ",
        "_",
        "not--vaild",
        "val!d",
        "not valid",
        "admin",
        "this_username_is_too_long_to_handle",
    ],
)
def test_invalid_names(username):
    """Test that correct usernames are stored"""
    with pytest.raises(AssertionError):
        User(username=username, password="testpass")
    # and also if trying to change it from a valid one
    with pytest.raises(AssertionError):
        u = User(username=f"user{randint(100,999)}", password="testpass")
        u.username = username


@pytest.mark.parametrize(
    "username", ["ahmed2", "911agent", "Tr0ll", "_dude_", "koko_soso"]
)
def test_valid_names(username):
    """Test that correct usernames are stored"""
    User(username=username, password="testpass")
