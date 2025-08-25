# Week6/api/models.py
from __future__ import annotations
from typing import Dict, Any
from datetime import date, timedelta
from .db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token


class Product(db.Model):
    """
    Base SQLAlchemy model for a product in the inventory.
    Implements single-table inheritance for different product categories.
    """

    __tablename__ = "products"

    product_id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(100), nullable=False)
    quantity: int = db.Column(db.Integer, nullable=False, default=0)
    price: float = db.Column(db.Float, nullable=False)
    type: str = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "product",
        "polymorphic_on": type,
    }

    def get_total_value(self) -> float:
        """Calculate total value of this product."""
        return self.price * self.quantity

    def to_dict(self) -> Dict[str, str | int | float]:
        """
        Convert Product instance to dictionary for JSON responses.
        Returns:
            dict: Dictionary representation of the product.
        """
        return {
            "product_id": self.product_id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "type": self.type,
        }

    def __repr__(self) -> str:
        return f"<Product id={self.product_id} name={self.name} type={self.type}>"


class FoodProduct(Product):
    """Product type: Food (with expiry date)."""

    expiry_date: date = db.Column(db.Date, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "food",
    }

    def to_dict(self) -> Dict[str, str | int | float]:
        data = super().to_dict()
        data.update(
            {"expiry_date": self.expiry_date.isoformat() if self.expiry_date else None}
        )
        return data


class ElectronicProduct(Product):
    """Product type: Electronic (with warranty period in months)."""

    warranty_period: int = db.Column(db.Integer, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "electronic",
    }

    def to_dict(self) -> Dict[str, str | int | float]:
        data = super().to_dict()
        data.update({"warranty_period": self.warranty_period})
        return data


class BookProduct(Product):
    """Product type: Book (with author and pages)."""

    author: str = db.Column(db.String(100), nullable=True)
    pages: int = db.Column(db.Integer, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "book",
    }

    def to_dict(self) -> Dict[str, str | int | float]:
        data = super().to_dict()
        data.update({"author": self.author, "pages": self.pages})
        return data


class User(db.Model):
    """
    User model for authentication and role-based access control (RBAC).

    Attributes:
        id (int): Primary key.
        username (str): Unique username.
        password_hash (str): Hashed password.
        role (str): User role (admin, manager, viewer).
    """

    __tablename__ = "users"

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    password_hash: str = db.Column(db.String(200), nullable=False)
    role: str = db.Column(db.String(20), nullable=False, default="viewer")

    def set_password(self, password: str) -> None:
        """
        Hash and store a user's password.
        Args:
            password (str): Plaintext password.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Verify a plaintext password against the stored hash.
        Args:
            password (str): Plaintext password.
        Returns:
            bool: True if password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def generate_token(self, expires_in: int = 3600) -> str:
        """
        Generate a JWT token for the user.
        Args:
            expires_in (int): Expiry time in seconds (default: 3600).
        Returns:
            str: JWT access token.
        """
        return create_access_token(
            identity={"id": self.id, "username": self.username, "role": self.role},
            expires_delta=timedelta(seconds=expires_in),
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert user instance to dictionary (excluding password hash).
        Returns:
            dict: Dictionary representation of the user.
        """
        return {"id": self.id, "username": self.username, "role": self.role}

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username} role={self.role}>"
