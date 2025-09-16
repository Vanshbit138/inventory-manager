"""
Database storage utilities for queries, embeddings, and chat history (multi-tenant ready).
"""

import psycopg2
from pgvector.psycopg2 import register_vector
import logging
from scripts.constants import DATABASE_URL_WEEK8 as DATABASE_URL

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def store_query(
    text: str, embedding: list[float] | None = None, user_id: int | None = None
) -> None:
    """
    Store a user query and its embedding into the `documents` table.
    Kept for backward compatibility with embedding storage pipeline.
    """
    if embedding is None:
        embedding = []
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            register_vector(conn)
            with conn.cursor() as cur:
                insert_sql = "INSERT INTO documents (content, embedding, user_id) VALUES (%s, %s, %s)"
                cur.execute(insert_sql, (text, embedding, user_id))
            conn.commit()
        logger.info(
            "[store_query] Stored query in DB for user_id=%s: %s...", user_id, text[:50]
        )
    except Exception as e:
        logger.error("[store_query] Failed for user_id=%s: %s", user_id, str(e))


def store_chat_history(user_id: int, question: str, answer: str) -> None:
    """
    Store a chat interaction (question & answer) into a `chat_history` table.
    This is separate from embeddings and does not require vector storage.
    """
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                create_table_sql = """
                CREATE TABLE IF NOT EXISTS chat_history (
                    id SERIAL PRIMARY KEY,
                    user_id INT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
                cur.execute(create_table_sql)

                insert_sql = """
                INSERT INTO chat_history (user_id, question, answer)
                VALUES (%s, %s, %s);
                """
                cur.execute(insert_sql, (user_id, question, answer))
            conn.commit()
        logger.info(
            "[store_chat_history] Stored chat for user_id=%s: %s...",
            user_id,
            question[:50],
        )
    except Exception as e:
        logger.error("[store_chat_history] Failed for user_id=%s: %s", user_id, str(e))
