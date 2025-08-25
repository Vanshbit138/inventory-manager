# api/security/password.py
from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(plain: str) -> str:
    """
    Hash a plaintext password using Werkzeug's PBKDF2 algorithm.

    Args:
        plain (str): The raw password provided by the user.

    Returns:
        str: A secure, salted hash of the password suitable for storage in the database.

    Notes:
        - Uses PBKDF2 with SHA256 by default.
        - Automatically generates a salt, so you do not need to handle salting manually.
        - The output includes the method, salt, and hash, so it can be verified later.
    """
    return generate_password_hash(plain)


def verify_password(hash_: str, plain: str) -> bool:
    """
    Verify a plaintext password against a stored password hash.

    Args:
        hash_ (str): The hashed password stored in the database.
        plain (str): The plaintext password provided by the user during login.

    Returns:
        bool: True if the plaintext password matches the stored hash, False otherwise.

    Notes:
        - Prevents timing attacks by using constant-time string comparison internally.
        - Always compare using this function instead of manually checking hashes.
    """
    return check_password_hash(hash_, plain)
