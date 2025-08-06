from typing import List
from inventory_manager.models import Product


def log_error(message: str) -> None:
    """Logs parsing/validation errors."""
    with open("error.log", "a") as f:
        f.write(f"[ERROR] {message}\n")


def write_low_stock_report(products: List[Product], threshold: int = 10) -> None:
    """Writes low-stock products to text file."""
    with open("low_stock_report.txt", "w") as f:
        f.write("LOW STOCK REPORT\n")
        f.write("================\n")
        for p in products:
            if p.quantity < threshold:
                f.write(f"{p.product_name} (ID: {p.product_id}) — Qty: {p.quantity}\n")
