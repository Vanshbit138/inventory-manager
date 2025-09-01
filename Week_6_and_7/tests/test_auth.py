def test_register_and_login(client):
    """
    Test the full registration and login flow for a new user.

    Steps:
        1. Register a new user with a unique username and password.
        2. Attempt login with the same credentials.
        3. Assert successful registration and login, and check that both
           access and refresh tokens are returned.
    """
    resp = client.post("/auth/register", json={"username": "new", "password": "123"})
    assert resp.status_code == 201

    resp = client.post("/auth/login", json={"username": "new", "password": "123"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data and "refresh_token" in data


def test_register_conflict(client):
    """
    Test that registering the same username twice returns a conflict.

    Steps:
        1. Register a user with a given username.
        2. Attempt to register again with the same username.
        3. Assert that the second registration fails with HTTP 409.
    """
    client.post("/auth/register", json={"username": "dup", "password": "x"})
    resp = client.post("/auth/register", json={"username": "dup", "password": "x"})
    assert resp.status_code == 409


def test_login_invalid(client):
    """
    Test login attempts with invalid credentials.

    Scenarios:
        - Non-existent username.
        - Incorrect password for an existing username.

    Expectation:
        - Both attempts should return HTTP 401 Unauthorized.
    """
    resp = client.post("/auth/login", json={"username": "ghost", "password": "x"})
    assert resp.status_code == 401

    resp = client.post("/auth/login", json={"username": "viewer", "password": "wrong"})
    assert resp.status_code == 401


def test_login_missing_fields(client):
    """
    Test login with missing fields in the request payload.

    Expectation:
        - Server should respond with HTTP 422 Unprocessable Entity.
    """
    resp = client.post("/auth/login", json={})
    assert resp.status_code == 422


def test_refresh_flow(client, tokens):
    """
    Test refreshing JWT tokens using a valid refresh token.

    Steps:
        1. Login to get a valid refresh token.
        2. Use the refresh token to request new access and refresh tokens.
        3. Assert HTTP 200 and that both new tokens are returned.
    """
    login = client.post("/auth/login", json={"username": "viewer", "password": "pass"})
    refresh_token = login.get_json()["refresh_token"]

    resp = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data and "refresh_token" in data


def test_refresh_invalid_token(client):
    """
    Test that using an invalid refresh token fails.

    Expectation:
        - Server should respond with HTTP 401 Unauthorized.
    """
    resp = client.post("/auth/refresh", json={"refresh_token": "badtoken"})
    assert resp.status_code == 401


def test_expired_access_token(client, tokens):
    """
    Test behavior when using an expired access token.

    Expectation:
        - For public endpoints like viewing products, expired token
          should not prevent access.
    """
    resp = client.get("/products/", headers={"Authorization": "Bearer expired_token"})
    assert resp.status_code == 200


def test_missing_token(client):
    """
    Test accessing a public endpoint without providing a token.

    Expectation:
        - Public endpoints should allow access even if no token is provided.
    """
    resp = client.get("/products/")
    assert resp.status_code == 200


def test_invalid_token(client):
    """
    Test accessing a public endpoint with an invalid access token.

    Expectation:
        - Public endpoints should allow access even if the token is invalid.
    """
    resp = client.get("/products/", headers={"Authorization": "Bearer invalid"})
    assert resp.status_code == 200
