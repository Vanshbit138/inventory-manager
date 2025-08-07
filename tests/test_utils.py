import pytest
from unittest.mock import patch, mock_open
from inventory_manager.utils import log_error, write_low_stock_report
from inventory_manager.models import Product


def test_log_error_writes_to_file():
    """
    Test log_error() function.

    Verifies that the function opens 'error.log' in append mode
    and writes the formatted error message to it.
    """
    message = "This is a test error"
    mocked_file = mock_open()

    with patch("builtins.open", mocked_file):
        log_error(message)

    mocked_file.assert_called_once_with("error.log", "a")
    mocked_file().write.assert_called_once_with(f"[ERROR] {message}\n")


@pytest.mark.parametrize(
    "products, threshold, expected_in_output, expected_not_in_output",
    [
        # One low-stock product
        (
            [
                Product(product_id=1, product_name="Test Product 1", price=10.0, quantity=5),
                Product(product_id=2, product_name="Test Product 2", price=15.0, quantity=15),
            ],
            10,
            ["Test Product 1"],
            ["Test Product 2"],
        ),
        # Both products are low stock
        (
            [
                Product(product_id=3, product_name="Test Product A", price=20.0, quantity=3),
                Product(product_id=4, product_name="Test Product B", price=25.0, quantity=2),
            ],
            5,
            ["Test Product A", "Test Product B"],
            [],
        ),
        # No product is low stock
        (
            [
                Product(product_id=5, product_name="Test Product X", price=30.0, quantity=20),
                Product(product_id=6, product_name="Test Product Y", price=35.0, quantity=25),
            ],
            10,
            [],
            ["Test Product X", "Test Product Y"],
        ),
    ]
)
def test_write_low_stock_report_parametrized(products, threshold, expected_in_output, expected_not_in_output):
    """
    Parametrized test for write_low_stock_report() with different stock levels.

    Verifies the report includes only products below the threshold.
    """
    mocked_file = mock_open()

    with patch("builtins.open", mocked_file):
        write_low_stock_report(products, threshold=threshold)

    mocked_file.assert_called_once_with("low_stock_report.txt", "w")
    write_calls = mocked_file().write.call_args_list
    output = "".join(call.args[0] for call in write_calls)

    # Always check headers
    assert "LOW STOCK REPORT" in output
    assert "================" in output

    for product_name in expected_in_output:
        assert product_name in output

    for product_name in expected_not_in_output:
        assert product_name not in output


def test_write_low_stock_report_handles_empty_list():
    """
    Test write_low_stock_report() with no products.

    Verifies that the report header is written correctly even when
    the product list is empty.
    """
    products = []
    mocked_file = mock_open()

    with patch("builtins.open", mocked_file):
        write_low_stock_report(products)

    mocked_file.assert_called_once_with("low_stock_report.txt", "w")
    write_calls = mocked_file().write.call_args_list
    output = "".join(call.args[0] for call in write_calls)

    assert "LOW STOCK REPORT" in output
    assert "================" in output
