# scripts/storage.py
"""
Database storage utilities for queries and embeddings.
"""

import psycopg2
from pgvector.psycopg2 import register_vector
import logging

from constants import DATABASE_URL


def store_query(text: str, embedding: list[float]) -> None:
    """Store a user query and its embedding into the `documents` table."""
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            register_vector(conn)
            with conn.cursor() as cur:
                insert_sql = (
                    "INSERT INTO documents (content, embedding) VALUES (%s, %s)"
                )
                cur.execute(insert_sql, (text, embedding))
            conn.commit()
        logging.info("Stored query in DB: %s...", text[:50])
    except Exception as e:
        logging.error("Failed to store query: %s", str(e))
