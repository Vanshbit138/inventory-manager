# scripts/data_loader.py
"""
Load product data from the database.
Supports multi-tenancy by filtering products per user_id.
"""

import logging
import psycopg2
from typing import List, Dict
from dotenv import load_dotenv
from constants import DATABASE_URL_WEEK8, PRODUCT_TABLE

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)


def load_products(user_id: int = None) -> List[Dict[str, str]]:
    """
    Load products from Postgres.
    If user_id is provided, only load products belonging to that user.
    """
    try:
        logging.info("Connecting to database: %s", DATABASE_URL_WEEK8)
        with psycopg2.connect(DATABASE_URL_WEEK8) as conn:
            with conn.cursor() as cur:
                query = f"""
                    SELECT product_id, name, type, price, quantity,
                           expiry_date, warranty_period, author, pages
                    FROM {PRODUCT_TABLE}
                """
                if user_id is not None:
                    query += f" WHERE owner_id = {user_id}"

                cur.execute(query)
                rows = cur.fetchall()

        products = []
        for row in rows:
            (
                product_id,
                name,
                ptype,
                price,
                quantity,
                expiry_date,
                warranty_period,
                author,
                pages,
            ) = row

            description_parts = [
                f"A {ptype} product priced at {price} with quantity {quantity}."
            ]
            if expiry_date:
                description_parts.append(f"It expires on {expiry_date}.")
            if warranty_period:
                description_parts.append(f"It has a warranty of {warranty_period}.")
            if author:
                description_parts.append(f"Written by {author}.")
            if pages:
                description_parts.append(f"Contains {pages} pages.")

            description = " ".join(description_parts)

            products.append(
                {
                    "product_id": product_id,
                    "name": name,
                    "description": description,
                }
            )

        logging.info("Loaded %d products from database", len(products))
        return products

    except Exception as e:
        logging.error("Failed to load products: %s", str(e))
        return []


if __name__ == "__main__":
    # Example: load products for user 17
    products = load_products(user_id=17)
    for p in products[:5]:
        print(p)
