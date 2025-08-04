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
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        product = self._parse_row(row)
                        if product:
                            self.products.append(product)
                    except Exception as e:
                        log_error(f"[Data Error] Skipped row {row} due to: {e}")
        except FileNotFoundError:
            log_error(f"[File Error] File not found: {file_path}")
        except Exception as e:
            log_error(f"[Unexpected Error] Failed to load CSV: {e}")

    def _parse_row(self, row: dict) -> Optional[Product]:
        """Detect type and build appropriate Product subclass."""
        try:
            base_fields = {
                "product_id": int(row["product_id"]),
                "product_name": row["product_name"],
                "price": float(row["price"]),
                "quantity": int(row["quantity"]),
            }

            product_type = row.get("type", "").strip().lower()

            if product_type == "food":
                return FoodProduct(
                    **base_fields,
                    expiry_date=datetime.strptime(row["expiry_date"], "%Y-%m-%d").date()
                )
            elif product_type == "electronic":
                return ElectronicProduct(
                    **base_fields,
                    warranty_period=int(row["warranty_period"])
                )
            elif product_type == "book":
                return BookProduct(
                    **base_fields,
                    author=row["author"],
                    pages=int(row["pages"])
                )
            else:
                return Product(**base_fields)

        except KeyError as e:
            raise ValueError(f"Missing required field: {e}")
        except ValueError as e:
            raise ValueError(f"Invalid data format: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error in _parse_row: {e}")

    def generate_report(self) -> None:
        """Generates enhanced inventory summary report."""
        try:
            print("\nINVENTORY REPORT")
            total_value = 0
            total_quantity = 0
            max_value = 0
            max_product = None

            for product in self.products:
                product_value = product.get_total_value()
                total_value += product_value
                total_quantity += product.quantity

                if product_value > max_value:
                    max_value = product_value
                    max_product = product

            print(f"Total Products : {len(self.products)}")
            print(f"Total Quantity:  {total_quantity}")
            if max_product:
                print(f"Highest Sale Product: {max_product.product_name} (₹{max_value:.2f})")
            print(f"Total Inventory Value: ₹{total_value:.2f}")

            write_low_stock_report(self.products, threshold=10)

        except Exception as e:
            log_error(f"[Report Error] Failed to generate inventory report: {e}")
