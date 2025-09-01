# Week6/api/models.py
from __future__ import annotations
from datetime import date
from .db import db
from werkzeug.security import generate_password_hash, check_password_hash


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
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    owner = db.relationship("User", back_populates="products")

    __mapper_args__ = {
        "polymorphic_identity": "product",
        "polymorphic_on": type,
    }

    def get_total_value(self) -> float:
        """Calculate total value of this product."""
        return self.price * self.quantity

    def __repr__(self) -> str:
        return f"<Product id={self.product_id} name={self.name} type={self.type}>"


class FoodProduct(Product):
    """Product type: Food (with expiry date)."""

    expiry_date: date = db.Column(db.Date, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "food",
    }


class ElectronicProduct(Product):
    """Product type: Electronic (with warranty period in months)."""

    warranty_period: int = db.Column(db.Integer, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "electronic",
    }


class BookProduct(Product):
    """Product type: Book (with author and pages)."""

    author: str = db.Column(db.String(100), nullable=True)
    pages: int = db.Column(db.Integer, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "book",
    }


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
    products = db.relationship(
        "Product", back_populates="owner", cascade="all, delete-orphan"
    )

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

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username} role={self.role}>"
