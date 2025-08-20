from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from datetime import date


class ProductCreate(BaseModel):
    """Schema for creating a product."""

    name: str
    price: float = Field(..., gt=0, description="Product price, must be greater than 0")
    quantity: int = Field(..., ge=0, description="Quantity in stock, must be >= 0")
    type: Literal["food", "electronic", "book"]
    expiry_date: Optional[date] = None
    warranty_period: Optional[int] = None


class ProductUpdate(BaseModel):
    """Schema for updating a product (partial updates allowed)."""

    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    expiry_date: Optional[date] = None
    warranty_period: Optional[int] = None


class ProductResponse(BaseModel):
    """Schema for product response."""

    product_id: int
    name: str
    price: float
    quantity: int
    type: str
    expiry_date: Optional[date] = None
    warranty_period: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)  # replaces orm_mode = True
