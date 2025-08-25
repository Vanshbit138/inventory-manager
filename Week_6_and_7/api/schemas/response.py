from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class ProductResponse(BaseModel):
    """
    Schema for returning product data in API responses.

    Attributes:
        product_id (int): Unique ID of the product.
        name (str): Name of the product.
        price (float): Price of the product.
        quantity (int): Quantity in stock.
        type (str): Type of the product ("food", "electronic", "book").
        expiry_date (Optional[date]): Expiry date for food products.
        warranty_period (Optional[int]): Warranty period in months for electronic products.
        author (Optional[str]): Author name for book products.
        pages (Optional[int]): Number of pages for book products.
    """

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
