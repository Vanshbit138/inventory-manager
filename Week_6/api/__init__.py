from flask import Flask
from flask_migrate import Migrate
from .config import Config
from .db import db
from .routes import products_bp

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize DB + Migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # Register routes
    app.register_blueprint(products_bp, url_prefix="/products")

    return app
