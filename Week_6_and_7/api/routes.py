from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
from sqlalchemy.orm.session import Session
from .models import db, Product, FoodProduct, ElectronicProduct, BookProduct
from .schemas.request import (
    FoodProductCreate,
    ElectronicProductCreate,
    BookProductCreate,
    FoodProductUpdate,
    ElectronicProductUpdate,
    BookProductUpdate,
)
from .schemas.response import ProductResponse
from .security.decorators import jwt_required

products_bp = Blueprint("products", __name__, url_prefix="/products")


def get_create_schema_and_model(type_: str):
    """
    Helper function to get the request schema and SQLAlchemy model
    based on product type.

    Args:
        type_ (str): Product type ('food', 'electronic', 'book').

    Returns:
        tuple: (Pydantic schema class, SQLAlchemy model class) or (None, None)
    """
    if type_ == "food":
        return FoodProductCreate, FoodProduct
    elif type_ == "electronic":
        return ElectronicProductCreate, ElectronicProduct
    elif type_ == "book":
        return BookProductCreate, BookProduct
    return None, None


def get_update_schema(type_: str):
    """
    Helper function to get the update request schema based on product type.

    Args:
        type_ (str): Product type ('food', 'electronic', 'book').

    Returns:
        Pydantic schema class or None
    """
    if type_ == "food":
        return FoodProductUpdate
    elif type_ == "electronic":
        return ElectronicProductUpdate
    elif type_ == "book":
        return BookProductUpdate
    return None


# ----------------------
# GET all products
# ----------------------
@products_bp.route("/", methods=["GET"])
def get_all_products() -> tuple:
    """
    Retrieve all products from the database.

    Returns:
        tuple: JSON list of products and HTTP status code.
    """
    try:
        products = Product.query.all()
        result = [ProductResponse.model_validate(p).model_dump() for p in products]
        return jsonify(result), 200
    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Failed to fetch products"}), 500


# ----------------------
# GET single product
# ----------------------
@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id: int) -> tuple:
    """
    Retrieve a single product by its ID.

    Args:
        product_id (int): ID of the product to retrieve.

    Returns:
        tuple: JSON representation of product or error message.
    """
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(ProductResponse.model_validate(product).model_dump()), 200


# ----------------------
# POST create product
# ----------------------
@products_bp.route("/", methods=["POST"])
@jwt_required
def create_product() -> tuple:
    """
    Create a new product based on its type (food, electronic, or book).

    Returns:
        tuple: JSON representation of created product or error message.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    type_ = data.get("type")
    Schema, Model = get_create_schema_and_model(type_)
    if not Schema or not Model:
        return jsonify({"error": "Invalid product type"}), 400

    try:
        product_data = Schema(**data)
        product = Model(**product_data.model_dump(exclude={"type"}))
    except ValidationError as e:
        return jsonify({"validation_error": e.errors()}), 400

    try:
        session: Session = db.session
        session.add(product)
        session.commit()
        return jsonify(ProductResponse.model_validate(product).model_dump()), 201
    except SQLAlchemyError as e:
        session.rollback()
        current_app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Failed to create product"}), 500


# ----------------------
# PUT update product
# ----------------------
@products_bp.route("/<int:product_id>", methods=["PUT"])
@jwt_required
def update_product(product_id: int) -> tuple:
    """
    Update an existing product by its ID.

    Args:
        product_id (int): ID of the product to update.

    Returns:
        tuple: JSON representation of updated product or error message.
    """
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    type_ = product.type
    UpdateSchema = get_update_schema(type_)
    if not UpdateSchema:
        return jsonify({"error": "Invalid product type"}), 400

    try:
        update_data = UpdateSchema(**data)
    except ValidationError as e:
        return jsonify({"validation_error": e.errors()}), 400

    try:
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)

        session: Session = db.session
        session.commit()
        return jsonify(ProductResponse.model_validate(product).model_dump()), 200
    except SQLAlchemyError as e:
        session.rollback()
        current_app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Failed to update product"}), 500


# ----------------------
# DELETE product
# ----------------------
@products_bp.route("/<int:product_id>", methods=["DELETE"])
@jwt_required
def delete_product(product_id: int) -> tuple:
    """
    Delete a product by its ID.

    Args:
        product_id (int): ID of the product to delete.

    Returns:
        tuple: Success message or error message.
    """
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    try:
        session: Session = db.session
        session.delete(product)
        session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    except SQLAlchemyError as e:
        session.rollback()
        current_app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Failed to delete product"}), 500
