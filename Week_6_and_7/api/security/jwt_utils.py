# api/security/jwt_utils.py
import os
import time
import jwt
from typing import Dict, Any

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


def encode_jwt(sub: int, role: str, expires_in: int | None = None) -> str:
    """
    Generate a JSON Web Token (JWT) for authentication and authorization.

    Args:
        sub (int): Subject (typically the user ID).
        role (str): Role of the user (e.g., "admin", "manager", "viewer").
        expires_in (int | None): Expiration time in seconds. Defaults to value from
                                 environment variable JWT_EXPIRES_IN (default: 3600s = 1 hour).

    Returns:
        str: Encoded JWT string that can be sent to the client.

    Example:
        >>> encode_jwt(1, "admin", 600)
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

    Notes:
        - The payload contains `sub`, `role`, and `exp` (expiry timestamp).
        - Algorithm used: HS256 (HMAC with SHA-256).
    """
    exp = int(time.time()) + int(
        expires_in or int(os.environ.get("JWT_EXPIRES_IN", 3600))
    )
    payload = {"sub": sub, "role": role, "exp": exp}
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

    Notes:
        - Always call this inside a try/except block to handle expired or invalid tokens.
    """
    return jwt.decode(token, _secret(), algorithms=[ALGO])
