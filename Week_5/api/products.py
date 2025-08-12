from flask import current_app, jsonify, request
from . import products_bp
from inventory_manager.models import Product


@products_bp.route("/", methods=["GET"])
def get_all_products():
    inventory = current_app.config["inventory"]
    return jsonify([p.model_dump() for p in inventory.products])


@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    inventory = current_app.config["inventory"]
    product = next((p for p in inventory.products if p.product_id == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.model_dump())


@products_bp.route("/", methods=["POST"])
def add_product():
    inventory = current_app.config["inventory"]
    try:
        data = request.get_json()
        new_product = Product(**data)
        inventory.products.append(new_product)
        return jsonify({"message": "Product added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
