from flask import current_app, jsonify, request, Response
from . import products_bp
from inventory_manager.models import Product
from pydantic import ValidationError
from typing import Tuple, Any


@products_bp.route("/", methods=["GET"])
def get_all_products() -> Response:
    """
    Get a list of all products in the inventory.
    """
    inventory = current_app.config["inventory"]
    return jsonify([p.model_dump() for p in inventory.products])


@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id: int) -> Tuple[Response, int] | Response:
    """
    Retrieve a single product by its product_id.
    """
    inventory = current_app.config["inventory"]
    product = next((p for p in inventory.products if p.product_id == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.model_dump())


@products_bp.route("/", methods=["POST"])
def add_product() -> Tuple[Response, int]:
    """
    Add a new product to the inventory.
    """
    inventory = current_app.config["inventory"]
    try:
        data: dict[str, Any] = request.get_json()
        new_product = Product(**data)
        inventory.products.append(new_product)
        return jsonify({"message": "Product added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@products_bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id: int) -> Tuple[Response, int]:
    """
    Update an existing product's details with validation.
    """
    inventory = current_app.config["inventory"]
    product = next((p for p in inventory.products if p.product_id == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    try:
        data: dict[str, Any] = request.get_json()

        # Merge existing product data with updates
        updated_data: dict[str, Any] = product.model_dump()
        updated_data.update(data)

        # Validate with Pydantic
        validated_product = Product(**updated_data)

        # Update the product
        product.__dict__.update(validated_product.__dict__)

        return jsonify({"message": "Product updated"}), 200

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@products_bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id: int) -> Tuple[Response, int]:
    """
    Delete a product from the inventory.
    """
    inventory = current_app.config["inventory"]
    product = next((p for p in inventory.products if p.product_id == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    inventory.products.remove(product)
    return jsonify({"message": "Product deleted"}), 200
