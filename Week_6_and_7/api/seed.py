# api/seed.py
import csv
import os
from typing import Optional
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask import Flask
from .app import create_app
from .db import db
from .models import Product, FoodProduct, ElectronicProduct, BookProduct, User

app: Flask = create_app()


def create_product_from_row(row: dict) -> Optional[Product]:
    """
    Factory function to create a Product instance from a CSV row.

    Determines the correct subclass (FoodProduct, ElectronicProduct, BookProduct)
    based on the 'type' field in the CSV row. Skips rows that are invalid or incomplete.

    Args:
        row (dict): A dictionary representing a CSV row.

    Returns:
        Optional[Product]: An instance of a Product subclass if valid, else None.
    """
    try:
        product_type = row.get("type", "").strip().lower()
        name = row.get("product_name") or row.get("name")

        if not name or not row.get("price") or not row.get("quantity"):
            return None

        price = float(row["price"])
        quantity = int(row["quantity"])

        if price <= 0 or quantity < 0:
            return None

        if product_type == "food":
            if not row.get("expiry_date"):
                return None
            expiry_date = datetime.strptime(row["expiry_date"], "%Y-%m-%d").date()
            if expiry_date < datetime.today().date():
                return None
            return FoodProduct(
                name=name, price=price, quantity=quantity, expiry_date=expiry_date
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

        return None

    except (ValueError, KeyError) as e:
        print(f"Skipping row due to error: {e} → {row}")
        return None


def seed_db() -> None:
    """
    Seed the database with products from 'data/products.csv'.

    Ensures each product has a valid owner. Creates a default 'system' user if needed
    and assigns all seeded products to this user.

    Notes:
        - Uses Flask app context to access the database.
        - Handles FileNotFoundError if CSV is missing.
        - Rolls back the session on SQLAlchemy errors.
        - Commits successfully added products to the database.
    """
    csv_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "data", "products.csv")
    )

    with app.app_context():
        try:
            # Create default system user if it doesn't exist
            default_user = User.query.filter_by(username="system").first()
            if not default_user:
                default_user = User(username="system", role="admin")
                default_user.set_password("adminpass")
                db.session.add(default_user)
                db.session.commit()

            with open(csv_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    product = create_product_from_row(row)
                    if product:
                        # Assign owner
                        product.owner = default_user  # sets owner_id automatically
                        existing = Product.query.filter_by(name=product.name).first()
                        if not existing:  # avoid duplicates
                            db.session.add(product)

                db.session.commit()
                print("Database seeded successfully!")

        except FileNotFoundError:
            print(f"CSV file not found at {csv_path}")
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error during seeding: {e}")


if __name__ == "__main__":
    seed_db()
