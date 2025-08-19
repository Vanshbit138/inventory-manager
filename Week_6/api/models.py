# Week6/api/models.py
from __future__ import annotations
from typing import Dict
from datetime import date
from .db import db


class Product(db.Model):
    """
    Base SQLAlchemy model for a product in the inventory.
    Implements single-table inheritance for different product categories.
    """

    __tablename__ = "products"

    id: int = db.Column(db.Integer, primary_key=True)
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
        """Convert Product instance to dictionary for JSON responses."""
        return {
            "product_id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "type": self.type,
        }

    def __repr__(self) -> str:
        return f"<Product id={self.id} name={self.name} type={self.type}>"


class FoodProduct(Product):
    """Product type: Food (with expiry date)."""

    expiry_date: date = db.Column(db.Date, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "food",
    }

    def to_dict(self) -> Dict[str, str | int | float]:
        data = super().to_dict()
        data.update({"expiry_date": self.expiry_date.isoformat()})
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
