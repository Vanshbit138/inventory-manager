import pytest
from unittest.mock import patch, mock_open
from inventory_manager.utils import log_error, write_low_stock_report
from inventory_manager.models import Product


def test_log_error_writes_to_file():
    message = "This is a test error"

    mocked_file = mock_open()
    with patch("builtins.open", mocked_file):
        log_error(message)

    mocked_file.assert_called_once_with("error.log", "a")
    mocked_file().write.assert_called_once_with(f"[ERROR] {message}\n")


def test_write_low_stock_report_writes_expected_products():
    products = [
        Product(product_id=1, product_name="Test Product 1", price=10.0, quantity=5),
        Product(product_id=2, product_name="Test Product 2", price=15.0, quantity=15),
    ]

    mocked_file = mock_open()
    with patch("builtins.open", mocked_file):
        write_low_stock_report(products, threshold=10)

    mocked_file.assert_called_once_with("low_stock_report.txt", "w")
    write_calls = mocked_file().write.call_args_list

    output = "".join(call.args[0] for call in write_calls)
    assert "LOW STOCK REPORT" in output
    assert "Test Product 1" in output
    assert "Test Product 2" not in output  # Should be excluded as quantity >= threshold


def test_write_low_stock_report_handles_empty_list():
    products = []

    mocked_file = mock_open()
    with patch("builtins.open", mocked_file):
        write_low_stock_report(products)

    mocked_file.assert_called_once_with("low_stock_report.txt", "w")
    write_calls = mocked_file().write.call_args_list

    output = "".join(call.args[0] for call in write_calls)
    assert "LOW STOCK REPORT" in output
    assert "================" in output
