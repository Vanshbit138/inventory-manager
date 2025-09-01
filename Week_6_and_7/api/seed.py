import csv
import os
from typing import Optional
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask import Flask
from .app import create_app  # ✅ ensure correct import
from .db import db
from .models import Product, FoodProduct, ElectronicProduct, BookProduct

app: Flask = create_app()


def create_product_from_row(row: dict) -> Optional[Product]:
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
        print(f" Skipping row due to error: {e} → {row}")
        return None


def seed_db() -> None:
    csv_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "data", "products.csv")
    )

    with app.app_context():
        try:
            with open(csv_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    product = create_product_from_row(row)
                    if product:
                        existing = Product.query.filter_by(name=product.name).first()
                        if not existing:  # avoid duplicates
                            db.session.add(product)

                db.session.commit()
                print("Database seeded successfully!")

        except FileNotFoundError:
            print(f" CSV file not found at {csv_path}")
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f" Database error during seeding: {e}")


if __name__ == "__main__":
    seed_db()
