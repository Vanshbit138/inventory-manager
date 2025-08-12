from flask import Blueprint
from . import products  # noqa: F401

products_bp = Blueprint("products", __name__)
