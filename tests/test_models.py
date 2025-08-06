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
    product = Product(product_id=1, product_name="Notebook", price=100.0, quantity=5)
    assert product.get_total_value() == 500.0


def test_food_product_total_value():
    food = FoodProduct(
        product_id=2,
        product_name="Milk",
        price=50.0,
        quantity=2,
        expiry_date=date.today() + timedelta(days=10),
    )
    assert food.get_total_value() == 100.0


def test_electronic_product_total_value():
    electronic = ElectronicProduct(
        product_id=3,
        product_name="Headphones",
        price=1500.0,
        quantity=1,
        warranty_period=2,
    )
    assert electronic.get_total_value() == 1500.0


def test_book_product_total_value():
    book = BookProduct(
        product_id=4,
        product_name="Python 101",
        price=250.0,
        quantity=3,
        author="John Doe",
        pages=300,
    )
    assert book.get_total_value() == 750.0


# --------- Edge Case Tests ---------


def test_product_zero_price():
    with pytest.raises(ValidationError):
        Product(product_id=5, product_name="Freebie", price=0.0, quantity=10)


def test_product_negative_quantity():
    with pytest.raises(ValidationError):
        Product(product_id=6, product_name="Pen", price=10.0, quantity=-2)


def test_product_blank_name():
    with pytest.raises(ValidationError):
        Product(product_id=7, product_name="", price=10.0, quantity=1)


def test_product_whitespace_name():
    with pytest.raises(ValidationError):
        Product(product_id=13, product_name="   ", price=20.0, quantity=1)


def test_product_zero_id():
    with pytest.raises(ValidationError):
        Product(product_id=0, product_name="Zero", price=10.0, quantity=1)


def test_product_negative_id():
    with pytest.raises(ValidationError):
        Product(product_id=-1, product_name="Negative", price=10.0, quantity=1)


def test_food_product_expired_date():
    with pytest.raises(ValidationError):
        FoodProduct(
            product_id=8,
            product_name="Yogurt",
            price=30.0,
            quantity=2,
            expiry_date=date.today() - timedelta(days=1),
        )


def test_electronic_product_zero_warranty():
    with pytest.raises(ValidationError):
        ElectronicProduct(
            product_id=9,
            product_name="Speaker",
            price=2000.0,
            quantity=1,
            warranty_period=0,
        )


def test_electronic_product_negative_warranty():
    with pytest.raises(ValidationError):
        ElectronicProduct(
            product_id=10,
            product_name="Monitor",
            price=7000.0,
            quantity=1,
            warranty_period=-6,
        )


def test_book_product_zero_pages():
    with pytest.raises(ValidationError):
        BookProduct(
            product_id=11,
            product_name="Empty Book",
            price=100.0,
            quantity=2,
            author="Ghost Writer",
            pages=0,
        )


def test_book_product_blank_author():
    with pytest.raises(ValidationError):
        BookProduct(
            product_id=12,
            product_name="Mystery Book",
            price=120.0,
            quantity=1,
            author="",
            pages=100,
        )


def test_book_product_whitespace_author():
    with pytest.raises(ValidationError):
        BookProduct(
            product_id=14,
            product_name="Mystery Book",
            price=120.0,
            quantity=1,
            author="   ",
            pages=100,
        )
