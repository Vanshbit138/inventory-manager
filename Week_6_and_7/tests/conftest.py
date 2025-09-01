import pytest
import os
import sys

# Add Week_6_and_7 directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Week_6_and_7.api import create_app, db
from Week_6_and_7.api.models import User
from Week_6_and_7.api.config import TestingConfig


@pytest.fixture
def app():
    """
    Create a Flask test app with in-memory DB for isolated tests.
    """
    app = create_app(TestingConfig)

    with app.app_context():
        db.create_all()

        # Seed default users
        viewer = User(username="viewer", role="viewer")
        viewer.set_password("pass")

        manager = User(username="manager", role="manager")
        manager.set_password("pass")

        admin = User(username="admin", role="admin")
        admin.set_password("pass")

        db.session.add_all([viewer, manager, admin])
        db.session.commit()

        yield app

        # Teardown
        db.drop_all()


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()


def login_helper(client, username: str, password: str) -> str:
    """Login a user and return JWT access token."""
    resp = client.post("/auth/login", json={"username": username, "password": password})
    data = resp.get_json()
    return data["access_token"] if resp.status_code == 200 else None


@pytest.fixture
def tokens(client):
    """
    Return a dict of JWT tokens for seeded users.
    """
    return {
        "viewer": login_helper(client, "viewer", "pass"),
        "manager": login_helper(client, "manager", "pass"),
        "admin": login_helper(client, "admin", "pass"),
    }
