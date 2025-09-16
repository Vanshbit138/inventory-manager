# Week_6_and_7/api/__init__.py
import os
from dotenv import load_dotenv

# Load .env once from project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(env_path)

from flask import Flask
from flask_migrate import Migrate
from .config import Config
from .db import db
from .routes import products_bp
from .chat_routes import chat_bp

migrate = Migrate()


def create_app(config_class=Config):
    """Application factory that accepts a config class (default = Config)."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize DB + Migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(chat_bp, url_prefix="/chat")

    # Register documents blueprint
    from .documents import documents_bp

    app.register_blueprint(documents_bp, url_prefix="/documents")

    # Register auth blueprint
    from .security.auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
