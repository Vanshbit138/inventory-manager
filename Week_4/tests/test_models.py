from datetime import date, timedelta
import pytest
from pydantic import ValidationError
from inventory_manager.models import (
    Product,
    FoodProduct,
    ElectronicProduct,
    BookProduct,
)

# --------- Validity Tests ---------


def test_product_total_value():
    """
    Test that the total value of a valid generic Product is calculated correctly.

    Expected: price * quantity.
    """
    product = Product(product_id=1, product_name="Notebook", price=100.0, quantity=5)
    assert product.get_total_value() == 500.0


def test_food_product_total_value():
    """
    Test that a valid FoodProduct with a future expiry date calculates total value correctly.
    """
    food = FoodProduct(
        product_id=2,
        product_name="Milk",
        price=50.0,
        quantity=2,
        expiry_date=date.today() + timedelta(days=10),
    )
    assert food.get_total_value() == 100.0


def test_electronic_product_total_value():
    """
    Test that a valid ElectronicProduct with positive warranty calculates total value correctly.
    """
    electronic = ElectronicProduct(
        product_id=3,
        product_name="Headphones",
        price=1500.0,
        quantity=1,
        warranty_period=2,
    )
    assert electronic.get_total_value() == 1500.0


def test_book_product_total_value():
    """
    Test that a valid BookProduct with proper author and page count calculates total value correctly.
    """
    book = BookProduct(
        product_id=4,
        product_name="Python 101",
        price=250.0,
        quantity=3,
        author="John Doe",
        pages=300,
    )
    assert book.get_total_value() == 750.0


# --------- Parametrized Invalid Product Tests ---------


@pytest.mark.parametrize(
    "kwargs",
    [
        {"product_id": 5, "product_name": "Freebie", "price": 0.0, "quantity": 10},
        {"product_id": 6, "product_name": "Pen", "price": 10.0, "quantity": -2},
        {"product_id": 7, "product_name": "", "price": 10.0, "quantity": 1},
        {"product_id": 13, "product_name": "   ", "price": 20.0, "quantity": 1},
        {"product_id": 0, "product_name": "Zero", "price": 10.0, "quantity": 1},
        {"product_id": -1, "product_name": "Negative", "price": 10.0, "quantity": 1},
    ],
)
def test_invalid_product_fields(kwargs):
    """
    Parametrized test that ensures ValidationError is raised for invalid Product fields:
    - Zero or negative product_id
    - Zero price
    - Negative quantity
    - Blank or whitespace product name
    """
    with pytest.raises(ValidationError):
        Product(**kwargs)


def test_food_product_expired_date():
    """
    Test that a FoodProduct with a past expiry date raises a ValidationError.
    """
    with pytest.raises(ValidationError):
        FoodProduct(
            product_id=8,
            product_name="Yogurt",
            price=30.0,
            quantity=2,
            expiry_date=date.today() - timedelta(days=1),
        )


@pytest.mark.parametrize("warranty", [0, -1])
def test_electronic_product_invalid_warranty(warranty):
    """
    Parametrized test that ensures ValidationError is raised for invalid warranty values
    in ElectronicProduct (0 or negative).
    """
    with pytest.raises(ValidationError):
        ElectronicProduct(
            product_id=9,
            product_name="Speaker",
            price=2000.0,
            quantity=1,
            warranty_period=warranty,
        )


@pytest.mark.parametrize("author", ["", "   "])
def test_book_product_invalid_author(author):
    """
    Parametrized test that ensures ValidationError is raised for blank or whitespace-only
    author names in BookProduct.
    """
    with pytest.raises(ValidationError):
        BookProduct(
            product_id=12,
            product_name="Mystery Book",
            price=120.0,
            quantity=1,
            author=author,
            pages=100,
        )


def test_book_product_zero_pages():
    """
    Test that a BookProduct with zero pages raises a ValidationError.
    """
    with pytest.raises(ValidationError):
        BookProduct(
            product_id=11,
            product_name="Empty Book",
            price=100.0,
            quantity=2,
            author="Ghost Writer",
            pages=0,
        )
