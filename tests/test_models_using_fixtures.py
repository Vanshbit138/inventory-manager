# tests/test_product.py

from datetime import date, timedelta
import pytest
from pydantic import ValidationError
from inventory_manager.models import (
    Product,
    FoodProduct,
    ElectronicProduct,
    BookProduct,
)


# --------- Total Value Tests (Refactored with Fixtures) ---------


def test_product_total_value(sample_product):
    # Arrange done by fixture
    # Act
    total = sample_product.get_total_value()
    # Assert
    assert total == 500.0


def test_food_product_total_value(sample_food_product):
    assert sample_food_product.get_total_value() == 100.0


def test_electronic_product_total_value(sample_electronic_product):
    assert sample_electronic_product.get_total_value() == 1500.0


def test_book_product_total_value(sample_book_product):
    assert sample_book_product.get_total_value() == 750.0


# --------- Edge Case Tests (Intentionally Not Using Fixtures) ---------


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
