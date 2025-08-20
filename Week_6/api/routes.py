from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
from .models import db, Product, FoodProduct, ElectronicProduct, BookProduct
from .schemas import ProductCreate, ProductUpdate, ProductResponse

products_bp = Blueprint("products", __name__, url_prefix="/products")


@products_bp.route("/", methods=["GET"])
def get_all_products() -> tuple:
    """Retrieve all products."""
    try:
        products = Product.query.all()
        # Use Pydantic response model for consistency
        result = [ProductResponse.model_validate(p).model_dump() for p in products]
        return jsonify(result), 200
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Failed to fetch products"}), 500


@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id: int) -> tuple:
    """Retrieve a single product by its ID."""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(ProductResponse.model_validate(product).model_dump()), 200


@products_bp.route("/", methods=["POST"])
def create_product() -> tuple:
    """Create a new product."""
    data = request.get_json()
    try:
        product_data = ProductCreate(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    try:
        if product_data.type == "food":
            product = FoodProduct(
                **product_data.model_dump(
                    exclude={"type", "warranty_period"}  # food doesn't use warranty
                )
            )
        elif product_data.type == "electronic":
            product = ElectronicProduct(
                **product_data.model_dump(
                    exclude={"type", "expiry_date"}  # electronics don't use expiry_date
                )
            )
        elif product_data.type == "book":
            product = BookProduct(
                **product_data.model_dump(
                    exclude={
                        "type",
                        "expiry_date",
                        "warranty_period",
                    }  # books use neither
                )
            )
        else:
            return jsonify({"error": "Invalid product type"}), 400

        db.session.add(product)
        db.session.commit()

        return jsonify(ProductResponse.model_validate(product).model_dump()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Failed to create product"}), 500


@products_bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id: int) -> tuple:
    """Update an existing product."""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    try:
        # Validate partial update
        update_data = ProductUpdate(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    try:
        for key, value in update_data.model_dump(exclude_unset=True).items():
            if key == "type":  # Don't allow type change
                continue
            setattr(product, key, value)

        db.session.commit()
        return jsonify(ProductResponse.model_validate(product).model_dump()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Failed to update product"}), 500


@products_bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id: int) -> tuple:
    """Delete a product by its ID."""
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
