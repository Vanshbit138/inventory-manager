import csv
from typing import List, Optional
from datetime import datetime
from inventory_manager.models import Product, FoodProduct, ElectronicProduct, BookProduct
from inventory_manager.utils import log_error, write_low_stock_report


class Inventory:
    def __init__(self) -> None:
        self.products: List[Product] = []

    def load_from_csv(self, file_path: str) -> None:
        """Load inventory data and classify product types."""
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    product = self._parse_row(row)
                    if product:
                        self.products.append(product)
                except Exception as e:
                    log_error(f"Error parsing row {row}: {e}")

    def _parse_row(self, row: dict) -> Optional[Product]:
        """Detect type and build appropriate Product subclass."""
        base_fields = {
            "product_id": int(row["product_id"]),
            "product_name": row["product_name"],
            "price": float(row["price"]),
            "quantity": int(row["quantity"]),
        }

        product_type = row.get("type", "").strip().lower()

        if product_type == "food":
            return FoodProduct(**base_fields, expiry_date=datetime.strptime(row["expiry_date"], "%Y-%m-%d").date())
        elif product_type == "electronic":
            return ElectronicProduct(**base_fields, warranty_period=int(row["warranty_period"]))
        elif product_type == "book":
            return BookProduct(**base_fields, author=row["author"], pages=int(row["pages"]))
        else:
            return Product(**base_fields)

    def generate_report(self) -> None:
        """Prints inventory and writes low stock report."""
        print("\nINVENTORY REPORT")
        for product in self.products:
            print(f"- {product.product_name}: {product.quantity} x ₹{product.price:.2f} = ₹{product.get_total_value():.2f}")
        total = sum(p.get_total_value() for p in self.products)
        print(f"\nTotal Inventory Value: ₹{total:.2f}")
        write_low_stock_report(self.products, threshold=10)
