# api/security/decorators.py
from functools import wraps
from flask import request, jsonify
from ..models import User
from .jwt_utils import decode_jwt
from ..db import db


def jwt_required(view_func):
    """Decorator to protect routes and ensure the user provides a valid JWT."""

    @wraps(view_func)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", None)
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing or invalid"}), 401

        token = auth_header.split(" ")[1]
        try:
            payload = decode_jwt(token)
            request.user = db.session.get(User, payload["sub"])
            if not request.user:
                return jsonify({"error": "User not found"}), 404
        except Exception as e:
            return (
                jsonify({"error": "Invalid or expired token", "details": str(e)}),
                401,
            )

        return view_func(*args, **kwargs)

    return decorated


def roles_required(*roles):
    """Ensures that the current user has one of the allowed roles."""

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            user = getattr(request, "user", None)
            if not user:
                return jsonify({"error": "Unauthorized"}), 401

            if user.role not in roles:
                return jsonify({"error": "Forbidden, insufficient role"}), 403

            return view_func(*args, **kwargs)

        return wrapper

    return decorator


def get_current_user_id():
    """Extract user_id (sub) from JWT token."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise ValueError("Authorization header missing or invalid")

    token = auth_header.split(" ")[1]
    payload = decode_jwt(token)
    return payload["sub"]
