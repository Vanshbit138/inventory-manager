# Week_6/tests/test_routes_api.py
"""
Unit tests for Flask API routes in routes.py
Covers GET, POST, PUT, DELETE endpoints for Product and its variants (Food, Electronic, Book).
Includes handling of database errors, validation errors, missing data, and not-found cases.
"""

from unittest.mock import patch
import datetime
from sqlalchemy.exc import SQLAlchemyError
import os
import sys

# Add project root to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from Week_6_and_7.api.db import db
from Week_6_and_7.api.models import FoodProduct, ElectronicProduct, BookProduct


def test_get_all_products_success(client, test_app):
    """Test GET /products/ returns list of products."""
    with test_app.app_context():
        p1 = FoodProduct(
            name="Apple", price=1.2, quantity=10, expiry_date=datetime.date(2099, 1, 1)
        )
        db.session.add(p1)
        db.session.commit()

    res = client.get("/products/")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert any(p["name"] == "Apple" for p in data)


def test_get_all_products_db_error(client):
    """Test GET /products/ returns 500 if DB query fails."""
    with patch("Week_6_and_7.api.routes.Product.query") as mock_query:
        mock_query.all.side_effect = SQLAlchemyError("DB fail")
        res = client.get("/products/")
        assert res.status_code == 500
        assert res.get_json()["error"] == "Failed to fetch products"


def test_get_product_found(client, test_app):
    """Test GET /products/{id} returns a product if it exists."""
    with test_app.app_context():
        p = FoodProduct(
            name="Banana", price=1.5, quantity=5, expiry_date=datetime.date(2099, 1, 1)
        )
        db.session.add(p)
        db.session.commit()
        pid = p.product_id

    res = client.get(f"/products/{pid}")
    assert res.status_code == 200
    assert res.get_json()["name"] == "Banana"


def test_get_product_not_found(client):
    """Test GET /products/{id} returns 404 for non-existing product."""
    res = client.get("/products/9999")
    assert res.status_code == 404
    assert res.get_json()["error"] == "Product not found"


def test_create_product_success(client):
    """Test POST /products/ creates a product successfully."""
    res = client.post(
        "/products/",
        json={
            "type": "food",
            "name": "Orange",
            "price": 2.0,
            "quantity": 20,
            "expiry_date": "2099-01-01",
        },
    )
    assert res.status_code == 201
    assert res.get_json()["name"] == "Orange"


def test_create_product_no_body(client):
    """Test POST /products/ returns 400 when no input data is provided."""
    res = client.post("/products/", json={})
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_create_product_invalid_type(client):
    """Test POST /products/ returns 400 for invalid product type."""
    res = client.post("/products/", json={"type": "invalid", "name": "X"})
    assert res.status_code == 400
    assert res.get_json()["error"] == "Invalid product type"


def test_create_product_validation_error(client):
    """Test POST /products/ returns 400 when Pydantic validation fails."""
    res = client.post(
        "/products/",
        json={
            "type": "food",
            "name": "Orange",
            "price": "invalid",
            "quantity": 5,
            "expiry_date": "2099-01-01",
        },
    )
    assert res.status_code == 400
    assert "validation_error" in res.get_json()


def test_create_product_db_error(client):
    """Test POST /products/ returns 500 when DB commit fails."""
    with patch(
        "Week_6_and_7.api.routes.db.session.add", side_effect=SQLAlchemyError("DB fail")
    ):
        res = client.post(
            "/products/",
            json={
                "type": "food",
                "name": "BadDB",
                "price": 1.0,
                "quantity": 1,
                "expiry_date": "2099-01-01",
            },
        )
        assert res.status_code == 500
        assert res.get_json()["error"] == "Failed to create product"


def test_update_product_success(client, test_app):
    """Test PUT /products/{id} updates an existing product."""
    with test_app.app_context():
        p = ElectronicProduct(name="Laptop", price=1000, quantity=2, warranty_period=24)
        db.session.add(p)
        db.session.commit()
        pid = p.product_id

    res = client.put(f"/products/{pid}", json={"price": 1200})
    assert res.status_code == 200
    assert res.get_json()["price"] == 1200


def test_update_product_not_found(client):
    """Test PUT /products/{id} returns 404 for non-existing product."""
    res = client.put("/products/9999", json={"price": 500})
    assert res.status_code == 404
    assert res.get_json()["error"] == "Product not found"


def test_update_product_no_body(client, test_app):
    """Test PUT /products/{id} returns 400 when no update data is provided."""
    with test_app.app_context():
        p = ElectronicProduct(name="Phone", price=500, quantity=1, warranty_period=12)
        db.session.add(p)
        db.session.commit()
        pid = p.product_id

    res = client.put(f"/products/{pid}", json={})
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_update_product_validation_error(client, test_app):
    """Test PUT /products/{id} returns 400 when validation fails."""
    with test_app.app_context():
        p = ElectronicProduct(name="TV", price=800, quantity=3, warranty_period=24)
        db.session.add(p)
        db.session.commit()
        pid = p.product_id

    res = client.put(f"/products/{pid}", json={"price": "invalid"})
    assert res.status_code == 400
    assert "validation_error" in res.get_json()


def test_update_product_db_error(client, test_app):
    """Test PUT /products/{id} returns 500 when DB commit fails."""
    with test_app.app_context():
        p = ElectronicProduct(
            name="Microwave", price=200, quantity=1, warranty_period=12
        )
        db.session.add(p)
        db.session.commit()
        pid = p.product_id

    with patch(
        "Week_6_and_7.api.routes.db.session.commit",
        side_effect=SQLAlchemyError("DB fail"),
    ):
        res = client.put(f"/products/{pid}", json={"price": 300})
        assert res.status_code == 500
        assert res.get_json()["error"] == "Failed to update product"


def test_delete_product_success(client, test_app):
    """Test DELETE /products/{id} deletes a product."""
    with test_app.app_context():
        p = BookProduct(name="Book1", price=10, quantity=5, author="Auth", pages=100)
        db.session.add(p)
        db.session.commit()
        pid = p.product_id

    res = client.delete(f"/products/{pid}")
    assert res.status_code == 200
    assert res.get_json()["message"] == "Product deleted successfully"


def test_delete_product_not_found(client):
    """Test DELETE /products/{id} returns 404 for missing product."""
    res = client.delete("/products/9999")
    assert res.status_code == 404
    assert res.get_json()["error"] == "Product not found"


def test_delete_product_db_error(client, test_app):
    """Test DELETE /products/{id} returns 500 when DB delete fails."""
    with test_app.app_context():
        p = BookProduct(name="Book2", price=20, quantity=2, author="Auth", pages=200)
        db.session.add(p)
        db.session.commit()
        pid = p.product_id

    with patch(
        "Week_6_and_7.api.routes.db.session.delete",
        side_effect=SQLAlchemyError("DB fail"),
    ):
        res = client.delete(f"/products/{pid}")
        assert res.status_code == 500
        assert res.get_json()["error"] == "Failed to delete product"
