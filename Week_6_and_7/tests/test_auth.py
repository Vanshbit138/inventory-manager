def test_register_and_login(client):
    """New user can register and login."""
    resp = client.post("/auth/register", json={"username": "new", "password": "123"})
    assert resp.status_code == 201

    resp = client.post("/auth/login", json={"username": "new", "password": "123"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data and "refresh_token" in data


def test_register_conflict(client):
    """Registering same username twice should fail."""
    client.post("/auth/register", json={"username": "dup", "password": "x"})
    resp = client.post("/auth/register", json={"username": "dup", "password": "x"})
    assert resp.status_code == 409


def test_login_invalid(client):
    """Invalid login attempts."""
    resp = client.post("/auth/login", json={"username": "ghost", "password": "x"})
    assert resp.status_code == 401

    resp = client.post("/auth/login", json={"username": "viewer", "password": "wrong"})
    assert resp.status_code == 401


def test_login_missing_fields(client):
    resp = client.post("/auth/login", json={})
    assert resp.status_code == 422


def test_refresh_flow(client, tokens):
    """Valid refresh returns new tokens."""
    login = client.post("/auth/login", json={"username": "viewer", "password": "pass"})
    refresh_token = login.get_json()["refresh_token"]

    resp = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data and "refresh_token" in data


def test_refresh_invalid_token(client):
    resp = client.post("/auth/refresh", json={"refresh_token": "badtoken"})
    assert resp.status_code == 401


def test_expired_access_token(client, tokens):
    resp = client.get("/products/", headers={"Authorization": "Bearer expired_token"})
    assert resp.status_code == 200  # Anyone can view products


def test_missing_token(client):
    resp = client.get("/products/")
    assert resp.status_code == 200  # Public endpoint


def test_invalid_token(client):
    resp = client.get("/products/", headers={"Authorization": "Bearer invalid"})
    assert resp.status_code == 200  # Public endpoint
