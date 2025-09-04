# scripts/embedding.py
"""
Generate embeddings for a list of texts using OpenAI and store them in Postgres (pgvector).
"""

import os
import logging
from typing import List, Tuple

import psycopg2
from psycopg2.extras import execute_batch
from pgvector.psycopg2 import register_vector
from dotenv import load_dotenv

load_dotenv()
from openai import OpenAI

from constants import DATABASE_URL, EMBEDDING_MODEL
from embedded_sentences import EXAMPLE_SENTENCES

# ------------------ Setup ------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in environment or .env")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL_WEEK8 not set in environment or .env")

client = OpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)


# ------------------ Core Functions ------------------
def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for a list of texts using OpenAI."""
    try:
        logging.info("Requesting embeddings for %d texts", len(texts))
        resp = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
        return [item.embedding for item in resp.data]
    except Exception as e:
        logging.error("Failed to generate embeddings: %s", str(e))
        return []


def store_embeddings(pairs: List[Tuple[str, List[float]]]) -> None:
    """Store (text, embedding) pairs into the `documents` table."""
    try:
        logging.info("Storing %d embeddings in Postgres", len(pairs))
        with psycopg2.connect(DATABASE_URL) as conn:
            register_vector(conn)
            with conn.cursor() as cur:
                insert_sql = (
                    "INSERT INTO documents (content, embedding) VALUES (%s, %s)"
                )
                execute_batch(cur, insert_sql, pairs)
        logging.info("Inserted %d rows into documents", len(pairs))
    except Exception as e:
        logging.error("Failed to store embeddings: %s", str(e))


def main() -> None:
    """Main entry point."""
    embeddings = get_embeddings(EXAMPLE_SENTENCES)
    if not embeddings:
        logging.error("No embeddings generated, aborting.")
        return

    pairs = list(zip(EXAMPLE_SENTENCES, embeddings))
    store_embeddings(pairs)

    for text, emb in pairs:
        logging.info("Stored: %-50s embedding_len=%d", text[:50], len(emb))


if __name__ == "__main__":
    main()
