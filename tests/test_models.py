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
    """Test total value calculation for a valid generic product."""
    product = Product(product_id=1, product_name="Notebook", price=100.0, quantity=5)
    assert product.get_total_value() == 500.0


def test_food_product_total_value():
    """Test total value for a valid FoodProduct with a future expiry date."""
    food = FoodProduct(
        product_id=2,
        product_name="Milk",
        price=50.0,
        quantity=2,
        expiry_date=date.today() + timedelta(days=10),
    )
    assert food.get_total_value() == 100.0


def test_electronic_product_total_value():
    """Test total value for a valid ElectronicProduct with a positive warranty."""
    electronic = ElectronicProduct(
        product_id=3,
        product_name="Headphones",
        price=1500.0,
        quantity=1,
        warranty_period=2,
    )
    assert electronic.get_total_value() == 1500.0


def test_book_product_total_value():
    """Test total value for a valid BookProduct with proper author and page count."""
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
    """Product should raise ValidationError if price is zero."""
    with pytest.raises(ValidationError):
        Product(product_id=5, product_name="Freebie", price=0.0, quantity=10)


def test_product_negative_quantity():
    """Product should raise ValidationError if quantity is negative."""
    with pytest.raises(ValidationError):
        Product(product_id=6, product_name="Pen", price=10.0, quantity=-2)


def test_product_blank_name():
    """Product should raise ValidationError if name is blank."""
    with pytest.raises(ValidationError):
        Product(product_id=7, product_name="", price=10.0, quantity=1)


def test_product_whitespace_name():
    """Product should raise ValidationError if name is only whitespace."""
    with pytest.raises(ValidationError):
        Product(product_id=13, product_name="   ", price=20.0, quantity=1)


def test_product_zero_id():
    """Product should raise ValidationError if product_id is zero."""
    with pytest.raises(ValidationError):
        Product(product_id=0, product_name="Zero", price=10.0, quantity=1)


def test_product_negative_id():
    """Product should raise ValidationError if product_id is negative."""
    with pytest.raises(ValidationError):
        Product(product_id=-1, product_name="Negative", price=10.0, quantity=1)


def test_food_product_expired_date():
    """FoodProduct should raise ValidationError if expiry date is in the past."""
    with pytest.raises(ValidationError):
        FoodProduct(
            product_id=8,
            product_name="Yogurt",
            price=30.0,
            quantity=2,
            expiry_date=date.today() - timedelta(days=1),
        )


def test_electronic_product_zero_warranty():
    """ElectronicProduct should raise ValidationError if warranty is zero."""
    with pytest.raises(ValidationError):
        ElectronicProduct(
            product_id=9,
            product_name="Speaker",
            price=2000.0,
            quantity=1,
            warranty_period=0,
        )


def test_electronic_product_negative_warranty():
    """ElectronicProduct should raise ValidationError if warranty is negative."""
    with pytest.raises(ValidationError):
        ElectronicProduct(
            product_id=10,
            product_name="Monitor",
            price=7000.0,
            quantity=1,
            warranty_period=-6,
        )


def test_book_product_zero_pages():
    """BookProduct should raise ValidationError if page count is zero."""
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
    """BookProduct should raise ValidationError if author name is blank."""
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
    """BookProduct should raise ValidationError if author name is only whitespace."""
    with pytest.raises(ValidationError):
        BookProduct(
            product_id=14,
            product_name="Mystery Book",
            price=120.0,
            quantity=1,
            author="   ",
            pages=100,
        )
