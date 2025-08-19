import csv
from . import create_app
from .db import db
from .models import Product

app = create_app()


def seed_db():
    with app.app_context():
        db.create_all()  # Create tables if not exist
        with open("Week6/inventory.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                product = Product(
                    name=row["name"],
                    price=float(row["price"]),
                    quantity=int(row["quantity"]),
                )
                db.session.add(product)
            db.session.commit()
        print("Database seeded!")


if __name__ == "__main__":
    seed_db()
