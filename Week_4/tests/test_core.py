import pytest
from unittest.mock import patch, MagicMock
from inventory_manager.core import Inventory
from inventory_manager.models import FoodProduct, BookProduct, Product


def test_get_inventory_value(sample_product, sample_food_product, sample_book_product):
    """
    Unit test for Inventory.get_inventory_value().
    Verifies the total value is correctly summed from all products.
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
    Simulates a product that raises an exception during value calculation.
    Verifies fallback to 0.0 and graceful handling.
    """
    inventory = Inventory()
    faulty_product = MagicMock()
    faulty_product.get_total_value.side_effect = Exception("Boom")
    inventory.products = [faulty_product]
    assert inventory.get_inventory_value() == 0.0


@pytest.mark.parametrize(
    "row, expected_type",
    [
        (
            {
                "product_id": "1",
                "product_name": "Milk",
                "price": "50.0",
                "quantity": "10",
                "type": "food",
                "expiry_date": "2025-12-31",
            },
            FoodProduct,
        ),
        (
            {
                "product_id": "2",
                "product_name": "Python",
                "price": "100.0",
                "quantity": "5",
                "type": "book",
                "author": "Alice",
                "pages": "300",
            },
            BookProduct,
        ),
        (
            {
                "product_id": "3",
                "product_name": "Random",
                "price": "100.0",
                "quantity": "3",
                "type": "unknown",
            },
            Product,
        ),
    ],
)
def test_parse_row_valid_types(row, expected_type):
    """
    Parametrized test for _parse_row() validating correct product type instantiation.
    """
    inventory = Inventory()
    product = inventory._parse_row(row)
    assert isinstance(product, expected_type)


@pytest.mark.parametrize(
    "row, expected_msg",
    [
        (
            {
                "product_id": "4",
                "product_name": "Laptop",
                "price": "50000",
                # Missing quantity
                "type": "electronic",
                "warranty_period": "12",
            },
            "Missing required field",
        ),
        (
            {
                "product_id": "5",
                "product_name": "Table",
                "price": "NaN",
                "quantity": "2",
                "type": "book",
                "author": "Bob",
                "pages": "200",
            },
            "Invalid data format",
        ),
    ],
)
def test_parse_row_invalid_fields(row, expected_msg):
    """
    Parametrized test for invalid data in _parse_row() raising ValueError.
    """
    inventory = Inventory()
    with pytest.raises(ValueError, match=expected_msg):
        inventory._parse_row(row)


def test_parse_row_raises_runtime_error():
    """
    Verifies RuntimeError is raised when _parse_row() receives invalid input like None.
    """
    inventory = Inventory()
    row = None
    with pytest.raises(RuntimeError, match="Unexpected error in _parse_row"):
        inventory._parse_row(row)


@pytest.mark.parametrize(
    "csv_content, expected_type",
    [
        (
            "product_id,product_name,price,quantity,type,expiry_date\n"
            "1,Apple,10.0,20,food,2025-12-31\n",
            FoodProduct,
        ),
        (
            "product_id,product_name,price,quantity,type,author,pages\n"
            "2,Book,30.0,5,book,Alice,300\n",
            BookProduct,
        ),
    ],
)
def test_load_from_csv_reads_valid_products(csv_content, expected_type, tmp_path):
    """
    Parametrized test for load_from_csv() reading and parsing valid products.
    """
    file_path = tmp_path / "test.csv"
    file_path.write_text(csv_content)
    inventory = Inventory()
    inventory.load_from_csv(str(file_path))
    assert len(inventory.products) == 1
    assert isinstance(inventory.products[0], expected_type)


@patch("inventory_manager.core.log_error")
def test_load_from_csv_file_not_found(mock_log):
    """
    Verifies missing file logs an error.
    """
    inventory = Inventory()
    inventory.load_from_csv("non_existent.csv")
    mock_log.assert_called_once_with("[File Error] File not found: non_existent.csv")


@patch("inventory_manager.core.log_error")
def test_load_from_csv_unexpected_error(mock_log, tmp_path):
    """
    Verifies malformed CSV logs an unexpected error.
    """
    file_path = tmp_path / "bad.csv"
    file_path.write_text("invalid\x00text")
    inventory = Inventory()
    inventory.load_from_csv(str(file_path))
    assert mock_log.call_count == 1
    assert "Failed to load CSV" in mock_log.call_args[0][0]


@patch("inventory_manager.core.write_low_stock_report")
def test_generate_report_success(mock_write, capsys, sample_product):
    """
    Verifies report prints expected values and calls write_low_stock_report().
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
    Verifies that errors in report generation are logged correctly.
    """
    inventory = Inventory()
    inventory.products.append(sample_product)
    inventory.generate_report()
    mock_log.assert_called_once()
    assert "Failed to generate inventory report" in mock_log.call_args[0][0]
