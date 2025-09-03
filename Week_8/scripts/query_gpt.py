# scripts/query_gpt.py
"""
Interactive GPT query CLI:
- Accepts user queries in a loop
- Stores every query as an embedding in the database
- Uses OpenAI embeddings + chat completion API
- Exits only when the user types 'exit'
"""

import os
from dotenv import load_dotenv

load_dotenv()
from openai import OpenAI
import psycopg2
from pgvector.psycopg2 import register_vector

# Import constants
from constants import (
    CHAT_MODEL,
    EMBEDDING_MODEL,
    DOCUMENTS_TABLE,
    ENV_KEY_OPENAI,
    ENV_KEY_DB,
)

# ------------------ Setup ------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

OPENAI_API_KEY = os.getenv(ENV_KEY_OPENAI)
DATABASE_URL = os.getenv(ENV_KEY_DB)

if not OPENAI_API_KEY:
    raise RuntimeError(f"{ENV_KEY_OPENAI} is not set in environment or .env")
if not DATABASE_URL:
    raise RuntimeError(f"{ENV_KEY_DB} is not set in environment or .env")

client = OpenAI(api_key=OPENAI_API_KEY)


# ------------------ Functions ------------------
def get_embedding(text: str) -> list[float]:
    """Generate embedding for a single text."""
    resp = client.embeddings.create(model=EMBEDDING_MODEL, input=[text])
    return resp.data[0].embedding


def store_query(text: str, embedding: list[float]):
    """Store a user query and its embedding in the database."""
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            register_vector(conn)
            with conn.cursor() as cur:
                insert_sql = f"INSERT INTO {DOCUMENTS_TABLE} (content, embedding) VALUES (%s, %s)"
                cur.execute(insert_sql, (text, embedding))
        print(f" Stored query in DB: {text[:50]!r}")
    except Exception as e:
        print(" Database error:", e)


def ask_gpt(question: str, few_shot_example: bool = False) -> str:
    """Ask GPT a question and return the answer."""
    if few_shot_example:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Translate the following English sentences to French:\nHello -> Bonjour\nGood morning -> Bonjour",
            },
            {"role": "user", "content": question},
        ]
    else:
        messages = [{"role": "user", "content": question}]

    response = client.chat.completions.create(
        model=CHAT_MODEL, messages=messages, temperature=0
    )

    answer = response.choices[0].message.content
    usage = response.usage
    print("\nAnswer:\n", answer)
    print("\nTokens used:", usage.total_tokens)
    print("Approx cost (USD):", round(usage.total_tokens * 0.002 / 1000, 6))
    return answer


def main():
    print("=== GPT CLI (type 'exit' to quit) ===\n")
    while True:
        question = input("Enter your question: ")
        if question.strip().lower() == "exit":
            print("Exiting CLI. Goodbye!")
            break

        fs = input("Use few-shot example? (y/n): ").lower() == "y"

        # Store the query
        embedding = get_embedding(question)
        store_query(question, embedding)

        # Get GPT answer
        ask_gpt(question, few_shot_example=fs)


if __name__ == "__main__":
    main()
