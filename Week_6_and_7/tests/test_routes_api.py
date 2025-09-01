def test_viewer_can_get_products(client, tokens):
    resp = client.get(
        "/products/", headers={"Authorization": f"Bearer {tokens['viewer']}"}
    )
    assert resp.status_code == 200


def test_manager_can_create_product(client, tokens):
    product = {
        "name": "Laptop",
        "price": 1000,
        "quantity": 2,
        "type": "electronic",
        "warranty_period": 12,
    }
    resp = client.post(
        "/products/",
        json=product,
        headers={"Authorization": f"Bearer {tokens['manager']}"},
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["name"] == "Laptop"


def test_viewer_cannot_create_product(client, tokens):
    product = {
        "name": "Apple",
        "price": 3,
        "quantity": 10,
        "type": "food",
        "expiry_date": "2099-01-01",
    }
    resp = client.post(
        "/products/",
        json=product,
        headers={"Authorization": f"Bearer {tokens['viewer']}"},
    )
    assert resp.status_code == 403


def test_update_product_as_manager(client, tokens):
    # Create first
    product = {
        "name": "Book1",
        "price": 20,
        "quantity": 1,
        "type": "book",
        "author": "Author",
        "pages": 100,
    }
    resp = client.post(
        "/products/",
        json=product,
        headers={"Authorization": f"Bearer {tokens['manager']}"},
    )
    product_id = resp.get_json()["product_id"]

    # Update with full payload
    updated_product = {
        "name": "Book1",
        "price": 25,  # updated field
        "quantity": 1,
        "type": "book",
        "author": "Author",
        "pages": 100,
    }
    resp = client.put(
        f"/products/{product_id}",
        json=updated_product,
        headers={"Authorization": f"Bearer {tokens['manager']}"},
    )
    assert resp.status_code == 200
    assert resp.get_json()["price"] == 25


def test_update_product_forbidden_if_not_owner(client, tokens):
    # Admin creates
    product = {
        "name": "Book2",
        "price": 10,
        "quantity": 5,
        "type": "book",
        "author": "Auth",
        "pages": 50,
    }
    resp = client.post(
        "/products/",
        json=product,
        headers={"Authorization": f"Bearer {tokens['admin']}"},
    )
    product_id = resp.get_json()["product_id"]

    # Manager tries update → forbidden
    resp = client.put(
        f"/products/{product_id}",
        json={"price": 15},
        headers={"Authorization": f"Bearer {tokens['manager']}"},
    )
    assert resp.status_code == 403


def test_delete_product_as_admin(client, tokens):
    product = {
        "name": "TV",
        "price": 500,
        "quantity": 1,
        "type": "electronic",
        "warranty_period": 24,
    }
    resp = client.post(
        "/products/",
        json=product,
        headers={"Authorization": f"Bearer {tokens['admin']}"},
    )
    product_id = resp.get_json()["product_id"]

    resp = client.delete(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {tokens['admin']}"},
    )
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Product deleted successfully"


def test_delete_product_forbidden_for_manager(client, tokens):
    # Admin creates
    product = {
        "name": "Phone",
        "price": 600,
        "quantity": 1,
        "type": "electronic",
        "warranty_period": 12,
    }
    resp = client.post(
        "/products/",
        json=product,
        headers={"Authorization": f"Bearer {tokens['admin']}"},
    )
    product_id = resp.get_json()["product_id"]

    # Manager tries delete
    resp = client.delete(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {tokens['manager']}"},
    )
    assert resp.status_code == 403
