# api/security/decorators.py
from functools import wraps
from flask import request, jsonify
from ..models import User
from .jwt_utils import decode_jwt
from ..db import db


def jwt_required(view_func):
    """
    Decorator to protect routes and ensure the user provides a valid JWT.

    Usage:
        @jwt_required
        def protected_route():
            ...
    """

    @wraps(view_func)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", None)
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing or invalid"}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = decode_jwt(token)
            # Attach user info to request context
            request.user = User.query.get(payload["sub"])
            if not request.user:
                return jsonify({"error": "User not found"}), 404
        except Exception as e:
            return (
                jsonify({"error": "Invalid or expired token", "details": str(e)}),
                401,
            )

        # Call the original route handler
        return view_func(*args, **kwargs)

    return decorated


def roles_required(*roles):
    """
    Ensures that the current user has one of the allowed roles.
    Usage: @roles_required("admin", "manager")
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return jsonify({"error": "Missing or invalid token"}), 401

            token = auth_header.split(" ")[1]
            try:
                payload = decode_jwt(token)
                user = db.session.get(User, payload["sub"])
                if not user:
                    return jsonify({"error": "User not found"}), 401

                if user.role not in roles:
                    return jsonify({"error": "Forbidden, insufficient role"}), 403

                # attach user to request
                request.user = user
            except Exception as e:
                return jsonify({"error": str(e)}), 401

            return f(*args, **kwargs)

        return wrapper

    return decorator
