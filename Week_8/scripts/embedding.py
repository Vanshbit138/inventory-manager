# scripts/embedding.py
"""
Generate embeddings for a list of texts using OpenAI and store them in Postgres (pgvector).
"""

import os
import logging
from typing import List, Tuple
from dotenv import load_dotenv
from openai import OpenAI
import psycopg2
from psycopg2.extras import execute_batch
from pgvector.psycopg2 import register_vector

# Import constants
from constants import EMBEDDING_MODEL, DOCUMENTS_TABLE, ENV_KEY_OPENAI, ENV_KEY_DB

# ------------------ Setup ------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

OPENAI_API_KEY = os.getenv(ENV_KEY_OPENAI)
DATABASE_URL = os.getenv(ENV_KEY_DB)

if not OPENAI_API_KEY:
    raise RuntimeError(f"{ENV_KEY_OPENAI} not set in environment or .env")
if not DATABASE_URL:
    raise RuntimeError(f"{ENV_KEY_DB} not set in environment or .env")

client = OpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)

# ------------------ Config ------------------
SENTENCES: List[str] = [
    "Apples are a nutritious fruit with vitamins.",
    "Laptops are portable computers used for work and gaming.",
    "Harry Potter is a fantasy novel about a young wizard.",
]


# ------------------ Functions ------------------
def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Request embeddings for a list of texts from OpenAI."""
    logging.info("Requesting embeddings for %d texts", len(texts))
    resp = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in resp.data]


def store_embeddings(pairs: List[Tuple[str, List[float]]]) -> None:
    """Store (text, embedding) pairs into the database."""
    logging.info("Storing %d embeddings in Postgres", len(pairs))
    with psycopg2.connect(DATABASE_URL) as conn:
        register_vector(conn)
        with conn.cursor() as cur:
            insert_sql = (
                f"INSERT INTO {DOCUMENTS_TABLE} (content, embedding) VALUES (%s, %s)"
            )
            execute_batch(cur, insert_sql, pairs)
    logging.info("Inserted %d rows into %s", len(pairs), DOCUMENTS_TABLE)


def main() -> None:
    embeddings = get_embeddings(SENTENCES)
    pairs = list(zip(SENTENCES, embeddings))
    store_embeddings(pairs)

    for text, emb in pairs:
        logging.info("Stored: %-50s embedding_len=%d", text[:50], len(emb))


if __name__ == "__main__":
    main()
