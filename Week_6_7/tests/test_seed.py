import os
import tempfile
import pytest
import sys
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Week_6_7.api.seed import seed_db, create_product_from_row
from Week_6_7.api.models import db, Product, FoodProduct, ElectronicProduct, BookProduct
from Week_6_7.api.app import create_app


@pytest.fixture
def test_app():
    """Create and configure a new app instance for testing."""
    db_fd, db_path = tempfile.mkstemp()
    app = create_app()
    app.config.update(
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
        TESTING=True,
    )

    with app.app_context():
        db.create_all()
        yield app

    os.close(db_fd)
    os.unlink(db_path)


def test_seed_db_valid_data(test_app):
    """Happy path: valid rows should seed correctly."""
    with test_app.app_context():
        db.drop_all()
        db.create_all()

        seed_db()
        products = Product.query.all()

        assert len(products) == 4
        names = [p.name for p in products]
        assert set(names) == {"Apples", "Grapes", "Laptop", "Harry Potter"}


def test_create_product_invalid_rows():
    """Check that invalid rows are skipped."""
    # Missing name
    assert (
        create_product_from_row({"price": "10", "quantity": "5", "type": "food"})
        is None
    )

    # Zero/negative price or quantity
    assert (
        create_product_from_row(
            {"name": "Bad", "price": "0", "quantity": "5", "type": "food"}
        )
        is None
    )
    assert (
        create_product_from_row(
            {"name": "Bad", "price": "5", "quantity": "-1", "type": "food"}
        )
        is None
    )

    # Food: missing expiry date
    assert (
        create_product_from_row(
            {"name": "Apple", "price": "1.5", "quantity": "5", "type": "food"}
        )
        is None
    )

    # Food: expired
    expired_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    row = {
        "name": "Apple",
        "price": "1.5",
        "quantity": "5",
        "type": "food",
        "expiry_date": expired_date,
    }
    assert create_product_from_row(row) is None

    # Electronics: missing warranty
    row = {"name": "Laptop", "price": "1000", "quantity": "2", "type": "electronic"}
    assert create_product_from_row(row) is None

    # Book: missing author/pages
    row = {
        "name": "Book",
        "price": "20",
        "quantity": "3",
        "type": "book",
        "author": "Mike",
    }
    assert create_product_from_row(row) is None
    row = {
        "name": "Book",
        "price": "20",
        "quantity": "3",
        "type": "book",
        "pages": "200",
    }
    assert create_product_from_row(row) is None

    # Unknown type
    row = {"name": "Chair", "price": "20", "quantity": "3", "type": "furniture"}
    assert create_product_from_row(row) is None


def test_create_product_valid_variants():
    """Check valid Food, Electronics, and Book creation."""
    # Food valid
    future_date = (datetime.today() + timedelta(days=5)).strftime("%Y-%m-%d")
    row = {
        "name": "Orange",
        "price": "2.0",
        "quantity": "5",
        "type": "food",
        "expiry_date": future_date,
    }
    product = create_product_from_row(row)
    assert isinstance(product, FoodProduct)

    # Electronics valid
    row = {
        "name": "Phone",
        "price": "30000",
        "quantity": "2",
        "type": "electronic",
        "warranty_period": "24",
    }
    product = create_product_from_row(row)
    assert isinstance(product, ElectronicProduct)

    # Book valid
    row = {
        "name": "Novel",
        "price": "100",
        "quantity": "1",
        "type": "book",
        "author": "Author",
        "pages": "300",
    }
    product = create_product_from_row(row)
    assert isinstance(product, BookProduct)


def test_create_product_bad_values():
    """Test parsing errors (invalid int/float)."""
    row = {
        "name": "Broken",
        "price": "abc",
        "quantity": "5",
        "type": "food",
        "expiry_date": "2025-09-01",
    }
    assert create_product_from_row(row) is None

    row = {
        "name": "Broken",
        "price": "10",
        "quantity": "abc",
        "type": "food",
        "expiry_date": "2025-09-01",
    }
    assert create_product_from_row(row) is None


def test_seed_file_not_found(monkeypatch, test_app):
    """Simulate missing CSV file."""
    with test_app.app_context():
        monkeypatch.setattr("os.path.join", lambda *args: "nonexistent.csv")
        seed_db()  # should print "CSV file not found"


def test_seed_sqlalchemy_error(monkeypatch, test_app):
    """Simulate DB error during commit."""
    with test_app.app_context():

        def bad_commit():
            raise SQLAlchemyError("DB fail")

        monkeypatch.setattr(db.session, "commit", bad_commit)
        seed_db()  # should rollback gracefully
