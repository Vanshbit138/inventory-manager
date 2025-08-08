# tests/conftest.py

import pytest
from datetime import date, timedelta
from inventory_manager.models import (
    Product,
    FoodProduct,
    ElectronicProduct,
    BookProduct,
)


@pytest.fixture
def sample_product():
    """
    Fixture to provide a generic sample Product instance.
    """
    return Product(product_id=1, product_name="Notebook", price=100.0, quantity=5)


@pytest.fixture
def sample_food_product():
    """
    Fixture to provide a sample FoodProduct with an expiry date 10 days from today.
    """
    return FoodProduct(
        product_id=2,
        product_name="Milk",
        price=50.0,
        quantity=2,
        expiry_date=date.today() + timedelta(days=10),
    )


@pytest.fixture
def sample_electronic_product():
    """
    Fixture to provide a sample ElectronicProduct with a 2-month warranty.
    """
    return ElectronicProduct(
        product_id=3,
        product_name="Headphones",
        price=1500.0,
        quantity=1,
        warranty_period=2,
    )


@pytest.fixture
def sample_book_product():
    """
    Fixture to provide a sample BookProduct written by 'John Doe'.
    """
    return BookProduct(
        product_id=4,
        product_name="Python 101",
        price=250.0,
        quantity=3,
        author="John Doe",
        pages=300,
    )
