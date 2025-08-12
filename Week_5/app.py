from flask import Flask
from inventory_manager.core import Inventory
import os


def create_app(test_config=None):
    app = Flask(__name__)

    # Path to CSV from Week_3
    csv_path = os.path.join(
        os.path.dirname(__file__), "..", "Week_3", "data", "products.csv"
    )

    # Create Inventory instance and load data
    inventory = Inventory()
    inventory.load_from_csv(csv_path)

    # Store inventory in app context for blueprints
    app.config["inventory"] = inventory

    # Register blueprints
    from .api import products_bp

    app.register_blueprint(products_bp, url_prefix="/products")

    @app.route("/")
    def index():
        return {"message": "Inventory API is running"}

    return app
