# Week_6/tests/conftest.py

import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Week_6_7.api.app import create_app
from Week_6_7.api.db import db


@pytest.fixture(scope="module")
def test_app():
    """Create a Flask app for testing."""
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # in-memory test DB
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(test_app):
    """Flask test client that can call API routes."""
    return test_app.test_client()
