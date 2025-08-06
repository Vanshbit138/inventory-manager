import pytest
from unittest.mock import patch
from inventory_manager.core import Inventory
from inventory_manager.models import FoodProduct, BookProduct


def test_get_inventory_value(sample_product, sample_food_product, sample_book_product):
    # Arrange
    inventory = Inventory()
    inventory.products.extend(
        [sample_product, sample_food_product, sample_book_product]
    )

    # Act
    total_value = (
        sample_product.get_total_value()
        + sample_food_product.get_total_value()
        + sample_book_product.get_total_value()
    )

    # Assert
    assert total_value == inventory.get_inventory_value()


def test_parse_row_food_product():
    inventory = Inventory()
    row = {
        "product_id": "1",
        "product_name": "Milk",
        "price": "50.0",
        "quantity": "10",
        "type": "food",
        "expiry_date": "2025-12-31",
    }
    product = inventory._parse_row(row)
    assert isinstance(product, FoodProduct)
    assert product.product_name == "Milk"


def test_parse_row_book_product():
    inventory = Inventory()
    row = {
        "product_id": "2",
        "product_name": "Python 101",
        "price": "300.0",
        "quantity": "5",
        "type": "book",
        "author": "John Doe",
        "pages": "250",
    }
    product = inventory._parse_row(row)
    assert isinstance(product, BookProduct)
    assert product.author == "John Doe"


def test_parse_row_missing_field():
    inventory = Inventory()
    row = {
        "product_id": "3",
        "product_name": "Laptop",
        "price": "50000",
        # "quantity" is missing
        "type": "electronic",
        "warranty_period": "12",
    }
    with pytest.raises(ValueError, match="Missing required field"):
        inventory._parse_row(row)


def test_load_from_csv_reads_valid_products(tmp_path):
    csv_content = """product_id,product_name,price,quantity,type,expiry_date
1,Apple,10.0,20,food,2025-12-31
"""
    file_path = tmp_path / "products.csv"
    file_path.write_text(csv_content)

    inventory = Inventory()
    inventory.load_from_csv(str(file_path))

    assert len(inventory.products) == 1
    assert isinstance(inventory.products[0], FoodProduct)
    assert inventory.products[0].product_name == "Apple"


@patch("inventory_manager.core.write_low_stock_report")
def test_generate_report(
    mock_write_report, capsys, sample_product, sample_food_product
):
    inventory = Inventory()
    inventory.products.extend([sample_product, sample_food_product])

    inventory.generate_report()

    captured = capsys.readouterr()
    assert "INVENTORY REPORT" in captured.out
    assert "Total Products" in captured.out
    mock_write_report.assert_called_once()
