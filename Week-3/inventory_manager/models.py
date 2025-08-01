from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date


class Product(BaseModel):
    """Base product class with shared validation."""
    model_config = ConfigDict(strict=True)

    product_id: int = Field(..., ge=1)
    product_name: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=0)
    price: float = Field(..., gt=0)

    def get_total_value(self) -> float:
        """Calculate total value of this product."""
        return self.price * self.quantity


class FoodProduct(Product):
    """Product with expiry information."""
    expiry_date: date


class ElectronicProduct(Product):
    """Product with warranty."""
    warranty_period: int = Field(..., gt=0)  # months


class BookProduct(Product):
    """Book with author and pages."""
    author: str
    pages: int = Field(..., gt=0)
