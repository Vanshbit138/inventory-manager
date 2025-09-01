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
    """
    Create a new Flask app instance with a temporary SQLite database for testing.

    Yields:
        Flask app instance configured for testing.

    Notes:
        - The database file is removed after tests complete.
        - Ensures isolation of test environment from the production database.
    """
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
    """
    Provide a SQLAlchemy session for tests.

    Yields:
        SQLAlchemy session object.

    Notes:
        - Rolls back changes and resets database after each test to maintain isolation.
    """
    with test_app.app_context():
        yield db.session
        db.session.rollback()
        db.drop_all()
        db.create_all()


def test_user_password_hashing(session):
    """
    Test password hashing and verification for the User model.

    Steps:
        1. Create a User and set a password.
        2. Ensure the stored password hash is not equal to the plaintext password.
        3. Verify that check_password works for correct and incorrect passwords.
        4. Save to DB and retrieve to ensure persistence.
    """
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
    """
    Test that the Product model correctly calculates total value.

    Steps:
        1. Create a Product with price and quantity.
        2. Check that get_total_value returns correct total.
        3. Validate string representation of the Product.
    """
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
    """
    Test creation and retrieval of a FoodProduct.

    Steps:
        1. Create a FoodProduct with expiry date.
        2. Save to DB and retrieve.
        3. Ensure retrieved object has correct attributes and type.
    """
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
    """
    Test creation and retrieval of an ElectronicProduct.

    Steps:
        1. Create an ElectronicProduct with warranty_period.
        2. Save to DB and retrieve.
        3. Ensure attributes are correct and instance type is ElectronicProduct.
    """
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
    """
    Test creation and retrieval of a BookProduct.

    Steps:
        1. Create a BookProduct with author and pages.
        2. Save to DB and retrieve.
        3. Verify attributes and instance type.
    """
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
    """
    Test the relationship between User and Product and cascade deletes.

    Steps:
        1. Create a User and multiple Products linked to the user.
        2. Verify products are linked to user.
        3. Delete the user and ensure all related products are also deleted.
    """
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
