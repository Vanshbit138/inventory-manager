# scripts/query_gpt.py
"""
Interactive GPT query CLI with LangChain.

Responsibilities:
- Accepts user queries in a loop (CLI).
- Stores each query as an embedding in the Postgres database.
- Uses LangChain for structured GPT calls (zero-shot & few-shot).
- Exits only when the user types 'exit'.

SOLID Principles:
- SRP: Separate concerns (embedding, storage, querying, CLI loop).
- OCP: Code structured so adding new prompt templates or vector stores requires extension, not modification.
"""

import os
from typing import List

import psycopg2
from pgvector.psycopg2 import register_vector
from dotenv import load_dotenv

load_dotenv()
from openai import OpenAI

from constants import DATABASE_URL, EMBEDDING_MODEL, CHAT_MODEL

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

# ------------------ Environment Setup ------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set in environment or .env")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL_WEEK8 is not set in environment or .env")

# OpenAI client (for embeddings only)
client = OpenAI(api_key=OPENAI_API_KEY)

# LangChain chat model
chat_model = ChatOpenAI(model=CHAT_MODEL, temperature=0, api_key=OPENAI_API_KEY)
parser = StrOutputParser()

# ------------------ Prompt Templates ------------------
default_prompt = ChatPromptTemplate.from_messages([("user", "{question}")])

few_shot_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        (
            "user",
            "Translate the following English sentences to French:\n"
            "Hello -> Bonjour\nGood morning -> Bonjour",
        ),
        ("user", "{question}"),
    ]
)


# ------------------ Core Functions ------------------
def get_embedding(text: str) -> List[float]:
    """
    Generate an embedding for a given text using OpenAI.

    Args:
        text (str): Input text to embed.

    Returns:
        List[float]: Embedding vector representation of the text.
    """
    resp = client.embeddings.create(model=EMBEDDING_MODEL, input=[text])
    return resp.data[0].embedding


def store_query(text: str, embedding: List[float]) -> None:
    """
    Store a user query and its embedding into the `documents` table.

    Args:
        text (str): User query.
        embedding (List[float]): Corresponding embedding vector.
    """
    with psycopg2.connect(DATABASE_URL) as conn:
        register_vector(conn)
        with conn.cursor() as cur:
            insert_sql = "INSERT INTO documents (content, embedding) VALUES (%s, %s)"
            cur.execute(insert_sql, (text, embedding))
        conn.commit()
    print(f" Stored query in DB: {text[:50]!r}")


def ask_gpt(question: str, few_shot_example: bool = False) -> str:
    """
    Ask GPT a question using LangChain and return the structured answer.

    Args:
        question (str): The question to ask GPT.
        few_shot_example (bool): Whether to use a few-shot prompt template.

    Returns:
        str: GPT's answer.
    """
    prompt = few_shot_prompt if few_shot_example else default_prompt
    chain = prompt | chat_model | parser
    answer = chain.invoke({"question": question})

    print("\nAnswer:\n", answer)
    print("\nTokens used: (not available via LangChain wrapper)")
    print("Approx cost (USD): ~calculated if token counts are tracked manually")

    return answer


def cli_loop() -> None:
    """
    Run the interactive CLI loop.
    - Accepts user input.
    - Stores embeddings in DB.
    - Fetches GPT answers.
    """
    print("=== GPT CLI (LangChain-powered) (type 'exit' to quit) ===\n")
    while True:
        question = input("Enter your question: ")
        if question.strip().lower() == "exit":
            print("Exiting CLI. Goodbye!")
            break

        fs = input("Use few-shot example? (y/n): ").lower() == "y"

        # Store embedding
        embedding = get_embedding(question)
        store_query(question, embedding)

        # Get GPT answer
        ask_gpt(question, few_shot_example=fs)


if __name__ == "__main__":
    cli_loop()
