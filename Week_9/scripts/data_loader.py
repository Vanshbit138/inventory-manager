# scripts/db_loader.py
"""
Load product data (product_id, name, full description) from the database.
This will be used as input for chunking and embeddings in the RAG pipeline.
"""

import os
import logging
import psycopg2
from typing import List, Dict
from dotenv import load_dotenv
from constants import DATABASE_URL_WEEK8, PRODUCT_TABLE

# ------------------ Setup ------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)


def load_products() -> List[Dict[str, str]]:
    """
    Load products from Postgres.
    Build a synthetic description using all available fields.
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

            # Build a richer description
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
    products = load_products()
    for p in products[:5]:
        print(p)
