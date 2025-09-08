# api/security/jwt_utils.py
import os
import time
import jwt
from typing import Dict, Any
from flask import request

ALGO = "HS256"


def _secret() -> str:
    """
    Retrieve the secret key used for signing JWTs.

    Returns:
        str: The secret key from environment variable SECRET_KEY, or a fallback default.

    Notes:
        - Always set a strong, unpredictable SECRET_KEY in production (e.g., 32+ random bytes).
        - This secret must remain private, otherwise attackers could forge tokens.
    """
    return os.environ.get("SECRET_KEY", "dev-secret-override-me")


def encode_jwt(
    sub: int, role: str, token_type: str = "access", expires_in: int | None = None
) -> str:
    """
    Generate a JSON Web Token (JWT) for access or refresh.

    Args:
        sub (int): Subject (user ID).
        role (str): Role of the user (e.g., "admin", "manager", "viewer").
        token_type (str): "access" or "refresh".
        expires_in (int | None): Expiration time in seconds.
                                 Defaults: 3600s (1h) for access, 7 days for refresh.

    Returns:
        str: Encoded JWT string.
    """
    if token_type == "access":
        exp = int(time.time()) + int(
            expires_in or int(os.environ.get("JWT_EXPIRES_IN", 3600))
        )
    else:  # refresh
        exp = int(time.time()) + int(
            expires_in or int(os.environ.get("JWT_REFRESH_EXPIRES_IN", 604800))
        )

    payload = {"sub": str(sub), "role": role, "type": token_type, "exp": exp}
    return jwt.encode(payload, _secret(), algorithm=ALGO)


def decode_jwt(token: str) -> Dict[str, Any]:
    """
    Decode and verify a JWT.

    Args:
        token (str): Encoded JWT string provided by the client (usually via Authorization header).

    Returns:
        Dict[str, Any]: Decoded JWT payload containing at least:
            - "sub" (int): Subject (user ID).
            - "role" (str): User role.
            - "exp" (int): Expiry timestamp (Unix time).

    Raises:
        jwt.ExpiredSignatureError: If the token has expired.
        jwt.InvalidTokenError: If the token signature or structure is invalid.
    """
    return jwt.decode(token, _secret(), algorithms=[ALGO])


def encode_refresh_jwt(sub: int, expires_in: int | None = None) -> str:
    """
    Generate a Refresh JSON Web Token (JWT).

    Args:
        sub (int): Subject (user ID).
        expires_in (int | None): Expiration in seconds.
                                 Defaults to JWT_REFRESH_EXPIRES_IN (7 days).

    Returns:
        str: Encoded refresh JWT string.
    """
    exp = int(time.time()) + int(
        expires_in or int(os.environ.get("JWT_REFRESH_EXPIRES_IN", 604800))  # 7 days
    )
    payload = {"sub": str(sub), "type": "refresh", "exp": exp}
    return jwt.encode(payload, _secret(), algorithm=ALGO)


def get_jwt_identity() -> Dict[str, Any]:
    """
    Extract the current user's identity from the Authorization header JWT.

    Returns:
        Dict[str, Any]: Dictionary containing at least 'sub' (user id) and 'role'.

    Raises:
        ValueError: If Authorization header is missing or token is invalid.
    """
    auth_header = request.headers.get("Authorization", None)
    if not auth_header:
        raise ValueError("Authorization header missing")

    try:
        token_type, token = auth_header.split()
        if token_type.lower() != "bearer":
            raise ValueError("Authorization header must start with Bearer")
        payload = decode_jwt(token)
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError) as e:
        raise ValueError(f"Invalid token: {e}")
