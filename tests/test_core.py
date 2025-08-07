import pytest
from unittest.mock import patch, MagicMock
from inventory_manager.core import Inventory
from inventory_manager.models import FoodProduct, BookProduct, Product


def test_get_inventory_value(sample_product, sample_food_product, sample_book_product):
    """
    Unit test for Inventory.get_inventory_value().

    This test verifies that the inventory value is correctly calculated as the sum of
    get_total_value() for all products in the inventory.
    """
    inventory = Inventory()
    inventory.products.extend(
        [sample_product, sample_food_product, sample_book_product]
    )
    expected = (
        sample_product.get_total_value()
        + sample_food_product.get_total_value()
        + sample_book_product.get_total_value()
    )
    assert inventory.get_inventory_value() == expected


def test_get_inventory_value_handles_exception():
    """
    Unit test for Inventory.get_inventory_value() error handling.

    Simulates a product that raises an exception during value calculation.
    Verifies that the method returns 0.0 and handles the error gracefully.
    """
    inventory = Inventory()
    faulty_product = MagicMock()
    faulty_product.get_total_value.side_effect = Exception("Boom")
    inventory.products = [faulty_product]
    assert inventory.get_inventory_value() == 0.0


def test_parse_row_food_product():
    """
    Unit test for Inventory._parse_row() with 'food' type row.

    Verifies that a food product row is parsed correctly into a FoodProduct instance.
    """
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


def test_parse_row_book_product():
    """
    Unit test for Inventory._parse_row() with 'book' type row.

    Verifies that a book product row is parsed correctly into a BookProduct instance.
    """
    inventory = Inventory()
    row = {
        "product_id": "2",
        "product_name": "Python",
        "price": "100.0",
        "quantity": "5",
        "type": "book",
        "author": "Alice",
        "pages": "300",
    }
    product = inventory._parse_row(row)
    assert isinstance(product, BookProduct)


def test_parse_row_unknown_type():
    """
    Unit test for Inventory._parse_row() with unknown product type.

    Verifies that unknown types default to base Product instance.
    """
    inventory = Inventory()
    row = {
        "product_id": "3",
        "product_name": "Random",
        "price": "100.0",
        "quantity": "3",
        "type": "unknown",
    }
    product = inventory._parse_row(row)
    assert isinstance(product, Product)


def test_parse_row_missing_field():
    """
    Unit test for Inventory._parse_row() with missing fields.

    Verifies that ValueError is raised when a required field is missing.
    """
    inventory = Inventory()
    row = {
        "product_id": "4",
        "product_name": "Laptop",
        "price": "50000",
        # Missing quantity
        "type": "electronic",
        "warranty_period": "12",
    }
    with pytest.raises(ValueError, match="Missing required field"):
        inventory._parse_row(row)


def test_parse_row_invalid_price():
    """
    Unit test for Inventory._parse_row() with invalid data types.

    Verifies that a ValueError is raised when data parsing (e.g., float conversion) fails.
    """
    inventory = Inventory()
    row = {
        "product_id": "5",
        "product_name": "Table",
        "price": "NaN",
        "quantity": "2",
        "type": "book",
        "author": "Bob",
        "pages": "200",
    }
    with pytest.raises(ValueError, match="Invalid data format"):
        inventory._parse_row(row)


def test_parse_row_raises_runtime_error():
    """
    Unit test for Inventory._parse_row() handling completely invalid rows.

    Verifies that a RuntimeError is raised when row is None or completely malformed.
    """
    inventory = Inventory()
    row = None  # Will cause exception
    with pytest.raises(RuntimeError, match="Unexpected error in _parse_row"):
        inventory._parse_row(row)


def test_load_from_csv_reads_valid_products(tmp_path):
    """
    Unit test for Inventory.load_from_csv() with a valid CSV file.

    Verifies that valid CSV content is parsed into the appropriate product instances.
    """
    csv_content = """product_id,product_name,price,quantity,type,expiry_date
1,Apple,10.0,20,food,2025-12-31
"""
    file_path = tmp_path / "valid.csv"
    file_path.write_text(csv_content)

    inventory = Inventory()
    inventory.load_from_csv(str(file_path))

    assert len(inventory.products) == 1
    assert isinstance(inventory.products[0], FoodProduct)


@patch("inventory_manager.core.log_error")
def test_load_from_csv_file_not_found(mock_log):
    """
    Unit test for Inventory.load_from_csv() with non-existent file.

    Verifies that missing file errors are logged appropriately.
    """
    inventory = Inventory()
    inventory.load_from_csv("non_existent.csv")
    mock_log.assert_called_once_with("[File Error] File not found: non_existent.csv")


@patch("inventory_manager.core.log_error")
def test_load_from_csv_unexpected_error(mock_log, tmp_path):
    """
    Unit test for Inventory.load_from_csv() with unreadable file.

    Verifies that unexpected errors (e.g., binary corruption) are logged.
    """
    file_path = tmp_path / "bad.csv"
    file_path.write_text("invalid\x00text")  # Invalid chars

    inventory = Inventory()
    inventory.load_from_csv(str(file_path))
    assert mock_log.call_count == 1
    assert "Failed to load CSV" in mock_log.call_args[0][0]


@patch("inventory_manager.core.write_low_stock_report")
def test_generate_report_success(mock_write, capsys, sample_product):
    """
    Unit test for Inventory.generate_report().

    Verifies that report is printed and low-stock report is written.
    Uses capsys to capture stdout and assert report contents.
    """
    inventory = Inventory()
    inventory.products.append(sample_product)
    inventory.generate_report()
    captured = capsys.readouterr()
    assert "INVENTORY REPORT" in captured.out
    assert "Total Products" in captured.out
    mock_write.assert_called_once()


@patch("inventory_manager.core.write_low_stock_report", side_effect=Exception("Boom"))
@patch("inventory_manager.core.log_error")
def test_generate_report_logs_error(mock_log, mock_write, sample_product):
    """
    Unit test for Inventory.generate_report() error handling.

    Verifies that any failure in writing low stock report is logged properly.
    """
    inventory = Inventory()
    inventory.products.append(sample_product)
    inventory.generate_report()
    mock_log.assert_called_once()
    assert "Failed to generate inventory report" in mock_log.call_args[0][0]
