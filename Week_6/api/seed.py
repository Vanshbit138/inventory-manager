# import csv
# from . import create_app
# from .db import db
# from .models import Product

# app = create_app()


# def seed_db():
#     with app.app_context():
#         db.create_all()  # Create tables if not exist
#         with open("Week6/inventory.csv") as f:
#             reader = csv.DictReader(f)
#             for row in reader:
#                 product = Product(
#                     name=row["name"],
#                     price=float(row["price"]),
#                     quantity=int(row["quantity"]),
#                 )
#                 db.session.add(product)
#             db.session.commit()
#         print("Database seeded!")


# if __name__ == "__main__":
#     seed_db()

import csv
import os
from typing import Optional
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask import Flask
from . import create_app
from .db import db
from .models import Product, FoodProduct, ElectronicProduct, BookProduct


app: Flask = create_app()


def create_product_from_row(row: dict) -> Optional[Product]:
    """
    Factory function to create the correct Product subclass
    based on the 'type' field in the CSV row.

    Args:
        row (dict): A row from the CSV file.

    Returns:
        Product | None: A Product instance or None if invalid.
    """
    try:
        product_type = row.get("type", "").strip().lower()
        name = row.get("product_name") or row.get("name")

        if not name or not row.get("price") or not row.get("quantity"):
            # Skip incomplete rows
            return None

        price = float(row["price"])
        quantity = int(row["quantity"])

        if product_type == "food":
            expiry_date = (
                datetime.strptime(row["expiry_date"], "%Y-%m-%d").date()
                if row.get("expiry_date")
                else None
            )
            return FoodProduct(
                name=name,
                price=price,
                quantity=quantity,
                expiry_date=expiry_date,
            )

        elif product_type == "electronic":
            return ElectronicProduct(
                name=name,
                price=price,
                quantity=quantity,
                warranty_period=(
                    int(row["warranty_period"]) if row.get("warranty_period") else None
                ),
            )

        elif product_type == "book":
            return BookProduct(
                name=name,
                price=price,
                quantity=quantity,
                author=row.get("author"),
                pages=int(row["pages"]) if row.get("pages") else None,
            )

        else:
            # Warn for unknown product types
            print(f" Unknown product type '{product_type}' in row: {row}")
            return Product(
                name=name,
                price=price,
                quantity=quantity,
                type="product",
            )

    except (ValueError, KeyError) as e:
        print(f" Skipping row due to error: {e} → {row}")
        return None


def seed_db() -> None:
    """
    Seed the database with products from data/products.csv.
    Uses SQLAlchemy for persistence.
    """
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "products.csv")

    with app.app_context():
        try:
            with open(csv_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    product = create_product_from_row(row)
                    if product:
                        db.session.add(product)

                db.session.commit()
                print(" Database seeded successfully!")

        except FileNotFoundError:
            print(f" CSV file not found at {csv_path}")
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f" Database error during seeding: {e}")


if __name__ == "__main__":
    seed_db()
