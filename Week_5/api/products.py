from flask import current_app, jsonify, request
from . import products_bp
from inventory_manager.models import Product


@products_bp.route("/", methods=["GET"])
def get_all_products():
    """
    Get a list of all products in the inventory.

    Returns:
        Response: JSON array of all product data with status code 200.
    """
    inventory = current_app.config["inventory"]
    return jsonify([p.model_dump() for p in inventory.products])


@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    Retrieve a single product by its product_id.

    Args:
        product_id (int): The ID of the product to retrieve.

    Returns:
        Response: JSON representation of the product if found,
                  otherwise a JSON error message with 404 status.
    """
    inventory = current_app.config["inventory"]
    product = next((p for p in inventory.products if p.product_id == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.model_dump())


@products_bp.route("/", methods=["POST"])
def add_product():
    """
    Add a new product to the inventory.

    Expects JSON payload with product fields matching the Product model.

    Returns:
        Response: JSON message confirming addition with status 201,
                  or JSON error message with status 400 on failure.
    """
    inventory = current_app.config["inventory"]
    try:
        data = request.get_json()
        new_product = Product(**data)
        inventory.products.append(new_product)
        return jsonify({"message": "Product added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
