# tests/test_models.py
import os
import tempfile
import pytest
from datetime import date
from werkzeug.security import check_password_hash

from Week_6_and_7.api.app import create_app
from Week_6_and_7.api.models import (
    db,
    User,
    Product,
    FoodProduct,
    ElectronicProduct,
    BookProduct,
)


@pytest.fixture
def test_app():
    """Create a new app with a temporary DB for testing."""
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


@pytest.fixture
def session(test_app):
    """Provide a SQLAlchemy session inside app context."""
    with test_app.app_context():
        yield db.session
        db.session.rollback()
        db.drop_all()
        db.create_all()


def test_user_password_hashing(session):
    """Ensure password hashing and verification works."""
    user = User(username="alice", role="admin")
    user.set_password("secret123")

    assert user.password_hash != "secret123"
    assert check_password_hash(user.password_hash, "secret123")
    assert user.check_password("secret123") is True
    assert user.check_password("wrong") is False

    session.add(user)
    session.commit()

    loaded = User.query.filter_by(username="alice").first()
    assert loaded is not None
    assert loaded.check_password("secret123")


def test_product_total_value(session):
    """Ensure get_total_value works properly."""
    user = User(username="bob", role="manager")
    user.set_password("pass")
    session.add(user)
    session.commit()

    product = Product(
        name="Generic", price=10.0, quantity=3, owner=user, type="product"
    )
    session.add(product)
    session.commit()

    assert product.get_total_value() == 30.0
    assert str(product).startswith("<Product id=")


def test_food_product_creation(session):
    """Ensure FoodProduct is stored and retrieved properly."""
    user = User(username="carl", role="viewer")
    user.set_password("pass")
    session.add(user)
    session.commit()

    food = FoodProduct(
        name="Apple",
        price=2.5,
        quantity=10,
        expiry_date=date.today(),
        owner=user,
    )
    session.add(food)
    session.commit()

    loaded = FoodProduct.query.first()
    assert loaded.name == "Apple"
    assert isinstance(loaded, FoodProduct)


def test_electronic_product_creation(session):
    user = User(username="dana", role="viewer")
    user.set_password("pass")
    session.add(user)
    session.commit()

    laptop = ElectronicProduct(
        name="Laptop",
        price=1200.0,
        quantity=2,
        warranty_period=24,
        owner=user,
    )
    session.add(laptop)
    session.commit()

    loaded = ElectronicProduct.query.first()
    assert loaded.warranty_period == 24
    assert isinstance(loaded, ElectronicProduct)


def test_book_product_creation(session):
    user = User(username="eric", role="viewer")
    user.set_password("pass")
    session.add(user)
    session.commit()

    book = BookProduct(
        name="Harry Potter",
        price=50.0,
        quantity=5,
        author="J.K. Rowling",
        pages=400,
        owner=user,
    )
    session.add(book)
    session.commit()

    loaded = BookProduct.query.first()
    assert loaded.author == "J.K. Rowling"
    assert loaded.pages == 400
    assert isinstance(loaded, BookProduct)


def test_user_product_relationship_and_cascade(session):
    """Ensure products are linked to a user and cascade deletes work."""
    user = User(username="frank", role="admin")
    user.set_password("adminpass")

    product1 = Product(name="Item1", price=5.0, quantity=2, type="product", owner=user)
    product2 = Product(name="Item2", price=10.0, quantity=1, type="product", owner=user)

    session.add(user)
    session.add_all([product1, product2])
    session.commit()

    assert len(user.products) == 2

    # Deleting user should delete products
    session.delete(user)
    session.commit()

    assert Product.query.count() == 0
