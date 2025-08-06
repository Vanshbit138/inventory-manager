from pydantic import BaseModel, Field, ConfigDict, field_validator
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

    @field_validator("product_name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Product name cannot be blank or whitespace.")
        return v


class FoodProduct(Product):
    """Product with expiry information."""

    expiry_date: date

    @field_validator("expiry_date")
    @classmethod
    def validate_expiry_date(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("Expiry date cannot be in the past")
        return v


class ElectronicProduct(Product):
    """Product with warranty."""

    warranty_period: int = Field(..., gt=0)  # months


class BookProduct(Product):
    """Book with author and pages."""

    author: str = Field(..., min_length=1)
    pages: int = Field(..., gt=0)

    @field_validator("author")
    @classmethod
    def validate_author(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Author name cannot be blank or whitespace.")
        return v
