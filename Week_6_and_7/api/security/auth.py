# api/security/auth.py
from flask import Blueprint, request, jsonify
from ..db import db
from ..models import User
from ..security.jwt_utils import encode_jwt


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/register")
def register():
    """
    Register a new user.

    Endpoint:
        POST /auth/register

    Request JSON Payload:
        {
            "username": "johndoe",
            "password": "securepassword",
            "role": "admin"   # optional, defaults to "viewer"
        }

    Responses:
        201 Created:
            {
                "id": 1,
                "username": "johndoe",
                "role": "viewer"
            }
        409 Conflict:
            {"error": "username already registered"}
        422 Unprocessable Entity:
            {"error": "username and password required"}
    """
    data = request.get_json(force=True) or {}
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "viewer")  # default role

    if not username or not password:
        return jsonify({"error": "username and password required"}), 422

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "username already registered"}), 409

    user = User(username=username, role=role)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


@auth_bp.post("/login")
def login():
    """
    Authenticate user and return JWT.

    Payload:
        {
            "username": "<username>",
            "password": "<password>"
        }

    Responses:
        200 OK: Returns JWT token
        401 Unauthorized: Invalid credentials
        422 Unprocessable Entity: Missing username/password
    """
    data = request.get_json(force=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password required"}), 422

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "invalid credentials"}), 401

    token = encode_jwt(user.id, user.role)
    return jsonify({"access_token": token}), 200
