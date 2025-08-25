# Week_6/tests/test_models.py
import pytest
from datetime import date
from Week_6_and_7.api.models import Product, FoodProduct, ElectronicProduct, BookProduct


# ---------------- Fixtures ----------------
@pytest.fixture
def sample_food():
    """Provide a sample FoodProduct instance for testing."""
    return FoodProduct(
        name="Apple", price=2.5, quantity=10, expiry_date=date(2099, 1, 1)
    )


@pytest.fixture
def sample_electronic():
    """Provide a sample ElectronicProduct instance for testing."""
    return ElectronicProduct(name="Laptop", price=1000, quantity=2, warranty_period=24)


@pytest.fixture
def sample_book():
    """Provide a sample BookProduct instance for testing."""
    return BookProduct(name="Novel", price=20, quantity=5, author="Author", pages=300)


# ---------------- Base Product Tests ----------------
def test_product_get_total_value():
    """Test total value calculation of a generic Product."""
    product = Product(name="Generic", price=5, quantity=3, type="product")
    assert product.get_total_value() == 15


def test_product_to_dict():
    """Test dictionary serialization of a generic Product."""
    product = Product(name="Generic", price=5, quantity=3, type="product")
    d = product.to_dict()
    assert d["name"] == "Generic"
    assert d["price"] == 5
    assert d["quantity"] == 3
    assert d["type"] == "product"


def test_product_repr():
    """Test string representation of a generic Product."""
    product = Product(name="Generic", price=5, quantity=3, type="product")
    r = repr(product)
    assert "Generic" in r and "product" in r


# ---------------- FoodProduct Tests ----------------
def test_foodproduct_to_dict(sample_food):
    """Test dictionary serialization of a FoodProduct including expiry_date."""
    d = sample_food.to_dict()
    assert d["name"] == "Apple"
    assert d["expiry_date"] == "2099-01-01"
    assert d["type"] == "food"


def test_foodproduct_total_value(sample_food):
    """Test total value calculation of a FoodProduct."""
    assert sample_food.get_total_value() == 25


# ---------------- ElectronicProduct Tests ----------------
def test_electronicproduct_to_dict(sample_electronic):
    """Test dictionary serialization of an ElectronicProduct including warranty_period."""
    d = sample_electronic.to_dict()
    assert d["name"] == "Laptop"
    assert d["warranty_period"] == 24
    assert d["type"] == "electronic"


def test_electronicproduct_total_value(sample_electronic):
    """Test total value calculation of an ElectronicProduct."""
    assert sample_electronic.get_total_value() == 2000


# ---------------- BookProduct Tests ----------------
def test_bookproduct_to_dict(sample_book):
    """Test dictionary serialization of a BookProduct including author and pages."""
    d = sample_book.to_dict()
    assert d["name"] == "Novel"
    assert d["author"] == "Author"
    assert d["pages"] == 300
    assert d["type"] == "book"


def test_bookproduct_total_value(sample_book):
    """Test total value calculation of a BookProduct."""
    assert sample_book.get_total_value() == 100
