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
    Skips invalid rows (missing fields, invalid values).
    """
    try:
        product_type = row.get("type", "").strip().lower()
        name = row.get("product_name") or row.get("name")

        if not name or not row.get("price") or not row.get("quantity"):
            return None

        price = float(row["price"])
        quantity = int(row["quantity"])

        # Skip invalid values
        if price <= 0 or quantity < 0:
            return None

        if product_type == "food":
            if not row.get("expiry_date"):
                return None
            expiry_date = datetime.strptime(row["expiry_date"], "%Y-%m-%d").date()
            # Skip expired food
            if expiry_date < datetime.today().date():
                return None

            return FoodProduct(
                name=name,
                price=price,
                quantity=quantity,
                expiry_date=expiry_date,
            )

        elif product_type == "electronic":
            if not row.get("warranty_period"):
                return None
            return ElectronicProduct(
                name=name,
                price=price,
                quantity=quantity,
                warranty_period=int(row["warranty_period"]),
            )

        elif product_type == "book":
            if not row.get("author") or not row.get("pages"):
                return None
            return BookProduct(
                name=name,
                price=price,
                quantity=quantity,
                author=row["author"],
                pages=int(row["pages"]),
            )

        else:
            # Unknown product type → skip
            return None

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
