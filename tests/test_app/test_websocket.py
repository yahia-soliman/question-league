"""Testing of the Web Socket module"""

from unittest import mock

import pytest

from app.websocket import Room


@pytest.fixture
def mocksocket():
    ws = mock.MagicMock()
    ws.send = mock.MagicMock(return_value=0)
    return ws


@pytest.fixture
def emptyroom():
    """create an empty room"""
    return Room()


@pytest.fixture
def singleroom(emptyroom, mocksocket):
    """A room with a single player"""
    emptyroom.join({"user_id": "my_id", "socket": mocksocket})
    return emptyroom


@pytest.fixture
def douroom(singleroom, mocksocket):
    """A room with a single player"""
    singleroom.join({"user_id": "your_id", "socket": mocksocket})
    return singleroom


@pytest.mark.parametrize("roomid", ["hi", "there", ""])
def test_get(roomid):
    """get a non existent room"""
    assert Room.get(roomid) is None


def test_info(emptyroom):
    """Test the formatting of the room info object"""
    info = emptyroom.info
    assert type(info) is dict
    assert info["users"] == []
    assert info["categories"] == {}
    assert info["ready"] == 0


def test_join(singleroom):
    """Test the room.join method"""
    assert len(singleroom.users) == 1
    assert "my_id" in singleroom.users


def test_join2(douroom):
    assert len(douroom.users) == 2
    assert "my_id" in douroom.users
    assert "your_id" in douroom.users


def test_exit(douroom):
    """Test the exit method"""
    douroom.exit("my_id")
    assert len(douroom.users) == 1
    douroom.exit("your_id")
    assert len(douroom.users) == 0
    assert Room.get(douroom.id) is None
