from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.session import Session
from pydantic import ValidationError

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
from .security.decorators import jwt_required, roles_required
from .security.jwt_utils import get_jwt_identity  # fetch logged-in user


products_bp = Blueprint("products", __name__, url_prefix="/products")


def get_create_schema_and_model(type_: str):
    """Return request schema and model based on product type."""
    if type_ == "food":
        return FoodProductCreate, FoodProduct
    elif type_ == "electronic":
        return ElectronicProductCreate, ElectronicProduct
    elif type_ == "book":
        return BookProductCreate, BookProduct
    return None, None


def get_update_schema(type_: str):
    """Return update schema based on product type."""
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
    """Retrieve all products from the database."""
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
    """Retrieve a single product by its ID."""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(ProductResponse.model_validate(product).model_dump()), 200


# ----------------------
# POST create product
# ----------------------
@products_bp.route("/", methods=["POST"])
@jwt_required
@roles_required("manager", "admin")
def create_product() -> tuple:
    """Create a new product linked to the logged-in user."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    type_ = data.get("type")
    Schema, Model = get_create_schema_and_model(type_)
    if not Schema or not Model:
        return jsonify({"error": "Invalid product type"}), 400

    try:
        product_data = Schema(**data)
        current_user = get_jwt_identity()
        owner_id = int(current_user["sub"])  # use 'sub' from JWT as user ID
        product = Model(**product_data.model_dump(exclude={"type"}), owner_id=owner_id)
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
@roles_required("manager", "admin")
def update_product(product_id: int) -> tuple:
    """Update a product if the current user is the owner or admin."""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    current_user = get_jwt_identity()
    user_id = int(current_user["sub"])
    user_role = current_user["role"]

    if product.owner_id != user_id and user_role != "admin":
        return jsonify({"error": "Not authorized to update this product"}), 403

    type_ = product.type
    UpdateSchema = get_update_schema(type_)
    if not UpdateSchema:
        return jsonify({"error": "Invalid product type"}), 400

    try:
        update_data = UpdateSchema(**data)
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
    except ValidationError as e:
        return jsonify({"validation_error": e.errors()}), 400

    try:
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
@roles_required("admin")
def delete_product(product_id: int) -> tuple:
    """Delete a product if the current user is the owner or admin."""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    current_user = get_jwt_identity()
    user_id = int(current_user["sub"])
    user_role = current_user["role"]

    if product.owner_id != user_id and user_role != "admin":
        return jsonify({"error": "Not authorized to delete this product"}), 403

    try:
        session: Session = db.session
        session.delete(product)
        session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    except SQLAlchemyError as e:
        session.rollback()
        current_app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Failed to delete product"}), 500
