from unittest import mock

import pytest

from models import BaseModel


@pytest.mark.parametrize("attr", ["id", "created_at", "updated_at"])
@mock.patch("models.engine.sql.session")
def test_basic_props(session, attr):
    """Test that every initialized object hasd id, creation, updation date"""
    session.add = print
    obj = BaseModel()
    assert hasattr(obj, attr)


@pytest.mark.parametrize("method", ["save", "all"])
def test_class_methods(method):
    """Test that the base class have mandatory methods"""
    assert callable(getattr(BaseModel, method))
