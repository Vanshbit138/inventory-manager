from flask import Flask
from inventory_manager.core import Inventory
import os


def create_app(test_config=None):
    """
    Create and configure the Flask application instance.

    This function initializes the Flask app, loads inventory data
    from a CSV file, registers API blueprints, and sets up
    application configuration.

    Args:
        test_config (dict, optional): Configuration for testing purposes.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    # Path to CSV file containing product data from Week_3
    csv_path = os.path.join(
        os.path.dirname(__file__), "..", "Week_3", "data", "products.csv"
    )

    # Create an Inventory instance and load data from the CSV
    inventory = Inventory()
    inventory.load_from_csv(csv_path)

    # Store the inventory instance in Flask app config for access in blueprints
    app.config["inventory"] = inventory

    # Import and register the products blueprint under '/products' URL prefix
    from .api import products_bp

    app.register_blueprint(products_bp, url_prefix="/products")

    @app.route("/")
    def index():
        """
        Root endpoint to confirm API is running.

        Returns:
            dict: A simple JSON message.
        """
        return {"message": "Inventory API is running"}

    return app
