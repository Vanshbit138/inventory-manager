# tests/test_password.py
from Week_6_and_7.api.security.password import hash_password, verify_password


def test_hash_password_returns_hashed_string():
    """Ensure that hashing a password returns a non-empty string that is not equal to the original password."""
    plain_password = "my_secret_pass"
    hashed = hash_password(plain_password)

    assert isinstance(hashed, str)
    assert hashed != plain_password
    # instead of checking for pbkdf2 only, allow scrypt/pbkdf2/etc.
    assert "$" in hashed  # all Werkzeug hashes include parameters and salt


def test_verify_password_valid():
    """Ensure that verifying a valid password returns True."""
    plain_password = "my_secret_pass"
    hashed = hash_password(plain_password)

    assert verify_password(hashed, plain_password) is True


def test_verify_password_invalid():
    """Ensure that verifying an invalid password returns False."""
    plain_password = "my_secret_pass"
    hashed = hash_password(plain_password)

    assert verify_password(hashed, "wrong_password") is False
