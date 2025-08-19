from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.exc import SQLAlchemyError
from .models import db, Product, FoodProduct, ElectronicProduct, BookProduct

products_bp = Blueprint("products", __name__, url_prefix="/products")


@products_bp.route("/", methods=["GET"])
def get_all_products() -> tuple:
    """
    Retrieve all products from the database.

    Returns:
        tuple: JSON list of all products with status code 200 if successful,
               or an error message with status code 500 if a database error occurs.
    """
    try:
        products = Product.query.all()
        return jsonify([p.to_dict() for p in products]), 200
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Failed to fetch products"}), 500


@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id: int) -> tuple:
    """
    Retrieve a single product by its ID.

    Args:
        product_id (int): The unique identifier of the product.

    Returns:
        tuple: JSON representation of the product with status code 200 if found,
               or an error message with status code 404 if not found.
    """
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.to_dict()), 200


@products_bp.route("/", methods=["POST"])
def create_product() -> tuple:
    """
    Create a new product in the database.

    Request Body (JSON):
        type (str): The type of product ("food", "electronic", or "book").
        Other fields depend on the product type (e.g., name, price, quantity, etc.).

    Returns:
        tuple: JSON representation of the created product with status code 201,
               or an error message with status code 400/500 if validation fails
               or a database error occurs.
    """
    data = request.get_json()
    if not data or "type" not in data:
        return jsonify({"error": "Product type is required"}), 400

    try:
        product_type = data.pop("type").lower()
        if product_type == "food":
            product = FoodProduct(**data)
        elif product_type == "electronic":
            product = ElectronicProduct(**data)
        elif product_type == "book":
            product = BookProduct(**data)
        else:
            return jsonify({"error": "Invalid product type"}), 400

        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Failed to create product"}), 500


@products_bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id: int) -> tuple:
    """
    Update an existing product by its ID.

    Args:
        product_id (int): The unique identifier of the product.

    Request Body (JSON):
        Fields to update (except "type", which is not allowed to change).

    Returns:
        tuple: JSON representation of the updated product with status code 200,
               or an error message with status code 404 if not found,
               or 500 if a database error occurs.
    """
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    try:
        for key, value in data.items():
            if key == "type":  # Prevent changing product type
                continue
            if hasattr(product, key):
                setattr(product, key, value)

        db.session.commit()
        return jsonify(product.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Failed to update product"}), 500


@products_bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id: int) -> tuple:
    """
    Delete a product by its ID.

    Args:
        product_id (int): The unique identifier of the product.

    Returns:
        tuple: A success message with status code 200 if deleted,
               or an error message with status code 404 if not found,
               or 500 if a database error occurs.
    """
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Failed to delete product"}), 500
