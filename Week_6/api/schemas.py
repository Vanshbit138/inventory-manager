from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from datetime import date


# ----------------------
# Request Schemas
# ----------------------
class BaseProductCreate(BaseModel):
    """Base schema for creating a product."""

    product_id: int = Field(..., gt=0, description="Product id, must be > 0")
    name: str
    price: float = Field(..., gt=0, description="Product price, must be > 0")
    quantity: int = Field(..., ge=0, description="Quantity in stock, must be >= 0")
    type: Literal["food", "electronic", "book"]


class FoodProductCreate(BaseProductCreate):
    """Schema for creating a Food product."""

    expiry_date: date


class ElectronicProductCreate(BaseProductCreate):
    """Schema for creating an Electronic product."""

    warranty_period: int


class BookProductCreate(BaseProductCreate):
    """Schema for creating a Book product."""

    author: str
    pages: int


# ----------------------
# Update Schemas
# ----------------------
class BaseProductUpdate(BaseModel):
    """Base schema for updating a product (partial updates allowed)."""

    name: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)


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


# ----------------------
# Response Schema
# ----------------------
class ProductResponse(BaseModel):
    """Schema for returning product data in API responses."""

    product_id: int
    name: str
    price: float
    quantity: int
    type: str
    expiry_date: Optional[date] = None
    warranty_period: Optional[int] = None
    author: Optional[str] = None
    pages: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)  # ORM mode
