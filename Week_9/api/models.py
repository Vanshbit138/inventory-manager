# Week8/api/models.py
from __future__ import annotations
from datetime import date, datetime
from .db import db
from werkzeug.security import generate_password_hash, check_password_hash
from pgvector.sqlalchemy import Vector


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
        """Calculate total value of this product (price × quantity)."""
        return self.price * self.quantity

    def __repr__(self) -> str:
        return f"<Product id={self.product_id} name={self.name} type={self.type}>"


class FoodProduct(Product):
    """Product type: Food (with expiry date)."""

    expiry_date: date = db.Column(db.Date, nullable=True)
    __mapper_args__ = {"polymorphic_identity": "food"}


class ElectronicProduct(Product):
    """Product type: Electronic (with warranty period)."""

    warranty_period: int = db.Column(db.Integer, nullable=True)
    __mapper_args__ = {"polymorphic_identity": "electronic"}


class BookProduct(Product):
    """Product type: Book (with author and pages)."""

    author: str = db.Column(db.String(100), nullable=True)
    pages: int = db.Column(db.Integer, nullable=True)
    __mapper_args__ = {"polymorphic_identity": "book"}


class User(db.Model):
    """
    User model for authentication and RBAC.
    """

    __tablename__ = "users"

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    password_hash: str = db.Column(db.String(200), nullable=False)
    role: str = db.Column(db.String(20), nullable=False, default="viewer")

    products = db.relationship(
        "Product", back_populates="owner", cascade="all, delete-orphan"
    )
    documents = db.relationship(
        "Document", back_populates="owner", cascade="all, delete-orphan"
    )

    def set_password(self, password: str) -> None:
        """Hash and store a user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify a plaintext password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username} role={self.role}>"


class Document(db.Model):
    """
    Document model for storing embeddings using pgvector.
    """

    __tablename__ = "documents"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content: str = db.Column(db.Text, nullable=False)
    embedding = db.Column(Vector(1536))  # OpenAI text-embedding-3-small

    # NEW: Associate each document with a user for multi-tenancy
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    owner = db.relationship("User", back_populates="documents")

    def __repr__(self) -> str:
        return f"<Document id={self.id} user_id={self.user_id} content={self.content[:30]}...>"


class LLMCache(db.Model):
    """
    Cache table for storing LLM requests and responses.
    """

    __tablename__ = "llm_cache"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question: str = db.Column(db.Text, nullable=False, unique=True)
    answer: str = db.Column(db.Text, nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<LLMCache id={self.id} question={self.question[:30]}...>"
