# api/security/auth.py
from flask import Blueprint, request, jsonify
from ..db import db
from ..models import User
from ..security.jwt_utils import encode_jwt, encode_refresh_jwt, decode_jwt
from ..schemas.response import UserResponse
import jwt


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

    return jsonify(UserResponse.model_validate(user).model_dump()), 201


@auth_bp.post("/login")
def login():
    """
    Authenticate user and return both access & refresh tokens.

    Request:
        {
            "username": "<username>",
            "password": "<password>"
        }

    Responses:
        200 OK:
            {
                "access_token": "<jwt-access-token>",
                "refresh_token": "<jwt-refresh-token>"
            }
        401 Unauthorized:
            {"error": "invalid credentials"}
        422 Unprocessable Entity:
            {"error": "username and password required"}
    """
    data = request.get_json(force=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password required"}), 422

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "invalid credentials"}), 401

    access_token = encode_jwt(user.id, user.role)
    refresh_token = encode_refresh_jwt(user.id)

    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200


@auth_bp.post("/refresh")
def refresh():
    """
    Exchange a refresh token for a new access token.

    Request:
        {
            "refresh_token": "<jwt-refresh-token>"
        }

    Responses:
        200 OK:
            {"access_token": "<new-jwt-access-token>"}
        401 Unauthorized:
            {"error": "Invalid or expired refresh token"}
    """
    data = request.get_json(force=True) or {}
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        return jsonify({"error": "refresh_token required"}), 422

    try:
        payload = decode_jwt(refresh_token)
        if payload.get("type") != "refresh":
            return jsonify({"error": "Invalid token type"}), 401

        new_access_token = encode_jwt(
            payload["sub"], "viewer"
        )  # ideally lookup role from DB
        return jsonify({"access_token": new_access_token}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Refresh token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid refresh token"}), 401
