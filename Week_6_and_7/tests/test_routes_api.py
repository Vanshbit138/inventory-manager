def test_viewer_can_get_products(client, tokens):
    """
    Test that a viewer can fetch the list of products.

    Steps:
        - Send GET request to /products/ with viewer token.
        - Expect HTTP 200 OK response.
    """
    resp = client.get(
        "/products/", headers={"Authorization": f"Bearer {tokens['viewer']}"}
    )
    assert resp.status_code == 200


def test_manager_can_create_product(client, tokens):
    """
    Test that a manager can create a new electronic product.

    Steps:
        - Send POST request with product data using manager token.
        - Expect HTTP 201 Created response.
        - Verify returned product data matches input.
    """
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
    """
    Test that a viewer cannot create any product.

    Steps:
        - Send POST request with product data using viewer token.
        - Expect HTTP 403 Forbidden response.
    """
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
    """
    Test that a manager can update their own product.

    Steps:
        - Manager creates a product.
        - Update product price.
        - Expect HTTP 200 OK response.
        - Verify updated price is reflected.
    """
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

    updated_product = {
        "name": "Book1",
        "price": 25,
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
    """
    Test that updating a product by a non-owner (without admin role) is forbidden.

    Steps:
        - Admin creates a product.
        - Manager attempts to update the product.
        - Expect HTTP 403 Forbidden response.
    """
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

    resp = client.put(
        f"/products/{product_id}",
        json={"price": 15},
        headers={"Authorization": f"Bearer {tokens['manager']}"},
    )
    assert resp.status_code == 403


def test_delete_product_as_admin(client, tokens):
    """
    Test that an admin can delete any product.

    Steps:
        - Admin creates a product.
        - Delete the product.
        - Expect HTTP 200 OK response with success message.
    """
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
    """
    Test that a manager cannot delete a product they do not own.

    Steps:
        - Admin creates a product.
        - Manager attempts to delete it.
        - Expect HTTP 403 Forbidden response.
    """
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

    resp = client.delete(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {tokens['manager']}"},
    )
    assert resp.status_code == 403
