# tests/test_routes.py
import pytest
from inventory_manager.models import Product
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app

from inventory_manager.core import Inventory


@pytest.fixture
def client():
    """
    Creates a Flask test client with a pre-loaded in-memory inventory.
    """
    app = create_app()
    app.config["TESTING"] = True

    # Override inventory with test data
    test_inventory = Inventory()
    test_inventory.products = [
        Product(product_id=1, product_name="Notebook", price=100.0, quantity=5),
        Product(product_id=2, product_name="Pen", price=10.0, quantity=50),
    ]
    app.config["inventory"] = test_inventory

    with app.test_client() as client:
        yield client


# -------------------------
# GET /products/
# -------------------------
def test_get_all_products_success(client):
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["product_name"] == "Notebook"


def test_get_all_products_empty(client):
    client.application.config["inventory"].products = []
    response = client.get("/products/")
    assert response.status_code == 200
    assert response.get_json() == []


# -------------------------
# GET /products/<id>
# -------------------------
def test_get_product_success(client):
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Notebook"


def test_get_product_not_found(client):
    response = client.get("/products/999")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Product not found"


# -------------------------
# POST /products/
# -------------------------
def test_add_product_success(client):
    new_product = {
        "product_id": 3,
        "product_name": "Pencil",
        "price": 5.0,
        "quantity": 100,
    }
    response = client.post("/products/", json=new_product)
    assert response.status_code == 201
    assert response.get_json()["message"] == "Product added"
    assert any(
        p.product_id == 3 for p in client.application.config["inventory"].products
    )


def test_add_product_invalid_data(client):
    # Missing required fields
    bad_product = {"product_id": 4}
    response = client.post("/products/", json=bad_product)
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_add_product_invalid_type(client):
    # Wrong type for price
    bad_product = {
        "product_id": 5,
        "product_name": "Marker",
        "price": "not-a-float",
        "quantity": 10,
    }
    response = client.post("/products/", json=bad_product)
    assert response.status_code == 400
    assert "error" in response.get_json()


# -------------------------
# PUT /products/<id>
# -------------------------
def test_update_product_success(client):
    update_data = {"price": 150.0}
    response = client.put("/products/1", json=update_data)
    assert response.status_code == 200
    assert response.get_json()["message"] == "Product updated"
    assert client.application.config["inventory"].products[0].price == 150.0


def test_update_product_not_found(client):
    update_data = {"price": 150.0}
    response = client.put("/products/999", json=update_data)
    assert response.status_code == 404
    assert response.get_json()["error"] == "Product not found"


def test_update_product_invalid_data(client):
    update_data = {"price": "not-a-float"}
    response = client.put("/products/1", json=update_data)
    assert response.status_code == 400
    assert "error" in response.get_json()


# -------------------------
# DELETE /products/<id>
# -------------------------
def test_delete_product_success(client):
    response = client.delete("/products/1")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Product deleted"
    assert all(
        p.product_id != 1 for p in client.application.config["inventory"].products
    )


def test_delete_product_not_found(client):
    response = client.delete("/products/999")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Product not found"
