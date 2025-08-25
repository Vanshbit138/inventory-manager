from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date


# ----------------------
# Base request schemas
# ----------------------
class BaseProductCreate(BaseModel):
    """
    Base schema for creating a product.

    Attributes:
        name (str): Name of the product.
        price (float): Price of the product (must be > 0).
        quantity (int): Quantity in stock (must be >= 0).
        type (Literal["food", "electronic", "book"]): Type of the product.
    """

    name: str
    price: float = Field(..., gt=0, description="Product price, must be greater than 0")
    quantity: int = Field(..., ge=0, description="Quantity in stock, must be >= 0")
    type: Literal["food", "electronic", "book"]


class FoodProductCreate(BaseProductCreate):
    """
    Schema for creating a Food product.

    Attributes:
        expiry_date (date): Expiry date of the food product.
    """

    expiry_date: date


class ElectronicProductCreate(BaseProductCreate):
    """
    Schema for creating an Electronic product.

    Attributes:
        warranty_period (int): Warranty period in months.
    """

    warranty_period: int


class BookProductCreate(BaseProductCreate):
    """
    Schema for creating a Book product.

    Attributes:
        author (str): Author of the book.
        pages (int): Number of pages in the book.
    """

    author: str
    pages: int


# ----------------------
# Update schemas
# ----------------------
class BaseProductUpdate(BaseModel):
    """
    Base schema for updating a product (partial updates allowed).

    Attributes:
        name (Optional[str]): Updated name of the product.
        price (Optional[float]): Updated price (must be > 0).
        quantity (Optional[int]): Updated quantity (must be >= 0).
    """

    name: Optional[str] = None
    price: Optional[float] = Field(
        None, gt=0, description="Updated product price, must be > 0"
    )
    quantity: Optional[int] = Field(
        None, ge=0, description="Updated quantity in stock, must be >= 0"
    )


class FoodProductUpdate(BaseProductUpdate):
    """Schema for updating a Food product."""

    expiry_date: Optional[date] = None


class ElectronicProductUpdate(BaseProductUpdate):
    """Schema for updating an Electronic product."""

    warranty_period: Optional[int] = None


class BookProductUpdate(BaseProductUpdate):
    """Schema for updating a Book product."""

    author: Optional[str] = None
    pages: Optional[int] = None
