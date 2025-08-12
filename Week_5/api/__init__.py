"""
API blueprint package initializer.

This module sets up the 'products' blueprint by importing the
products routes module and initializing the Blueprint instance.

The 'products_bp' Blueprint is then used to register routes related
to product inventory management.
"""

from flask import Blueprint

products_bp = Blueprint("routes", __name__)

from . import routes  # noqa: F401
