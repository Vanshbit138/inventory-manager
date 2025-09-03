# scripts/embed_and_store.py
"""
Generate embeddings for a list of texts using OpenAI and store them in Postgres (pgvector).

Requirements:
  - OPENAI_API_KEY in environment or .env
  - DATABASE_URL in environment or .env, e.g. postgresql://user:pass@host:5432/dbname
  - Packages: openai, psycopg2-binary, pgvector, python-dotenv
"""

import os
import logging
from typing import List, Tuple

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from openai import OpenAI
import psycopg2
from psycopg2.extras import execute_batch
from pgvector.psycopg2 import register_vector

# ------------------ Setup ------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL_WEEK8")

if not OPENAI_API_KEY:
    raise RuntimeError(" OPENAI_API_KEY not set in environment or .env")
if not DATABASE_URL:
    raise RuntimeError(" DATABASE_URL not set in environment or .env")

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
def get_embeddings(
    texts: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """
    Request embeddings for a list of texts from OpenAI.
    Returns a list of embedding vectors.
    """
    logging.info("Requesting embeddings for %d texts", len(texts))
    try:
        resp = client.embeddings.create(model=model, input=texts)
        return [item.embedding for item in resp.data]
    except Exception as e:
        logging.error("Error fetching embeddings: %s", e)
        raise


def store_embeddings(pairs: List[Tuple[str, List[float]]]) -> None:
    """
    Store (text, embedding) pairs into the `documents` table.
    Uses pgvector's psycopg2 adapter for automatic mapping.
    """
    logging.info("Storing %d embeddings in Postgres", len(pairs))
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            register_vector(conn)
            with conn.cursor() as cur:
                insert_sql = (
                    "INSERT INTO documents (content, embedding) VALUES (%s, %s)"
                )
                execute_batch(cur, insert_sql, pairs)
        logging.info(" Inserted %d rows into documents", len(pairs))
    except Exception as e:
        logging.error("Database error: %s", e)
        raise


def main() -> None:
    embeddings = get_embeddings(SENTENCES)
    pairs = list(zip(SENTENCES, embeddings))
    store_embeddings(pairs)

    for text, emb in pairs:
        logging.info("Stored: %-50s embedding_len=%d", text[:50], len(emb))


if __name__ == "__main__":
    main()
