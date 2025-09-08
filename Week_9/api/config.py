import os
from dotenv import load_dotenv

# Load .env from project root
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(env_path)


class Config:
    """Base configuration with default settings."""

    # Use a specific DATABASE_URL for Week 8, fallback to general DATABASE_URL
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_WEEK8") or os.getenv(
        "DATABASE_URL"
    )
    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError(
            "DATABASE_URL_WEEK8 or DATABASE_URL is not set! Check your .env file."
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_WEEK8")  # Use Week 8 DB


class TestingConfig(Config):
    """Testing configuration (uses in-memory SQLite)."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "test-secret"


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
