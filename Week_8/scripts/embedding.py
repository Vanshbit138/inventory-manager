# scripts/ingest_embeddings.py
"""
Generate embeddings for product data and store them in PGVector.
Skips creation if embeddings already exist in the database.
"""

import logging
import os
from typing import List, Dict
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.documents import Document

from data_loader import load_products
from constants import EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP

# ---------------- Setup ----------------
load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in environment or .env")


def embed_and_store(
    products: List[Dict], collection_name: str = "product_embeddings"
) -> PGVector:
    """
    Generate embeddings for product data and store them in PGVector.
    If embeddings already exist in the collection, skip creation.
    """
    db_url = os.getenv("DATABASE_URL_WEEK8")
    if not db_url:
        raise ValueError("DATABASE_URL_WEEK8 not found in environment variables")

    logger.info("Initializing OpenAI embeddings...")
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)

    # ---------------- Check if embeddings already exist ----------------
    vector_store = PGVector(
        collection_name=collection_name,
        connection_string=db_url,
        embedding_function=embeddings,
    )

    try:
        existing_docs = vector_store.similarity_search("test", k=1)
        if existing_docs:
            logger.info(
                "Embeddings already exist in collection '%s'. Skipping creation.",
                collection_name,
            )
            return vector_store
    except Exception:
        logger.info("No existing embeddings found. Creating new ones...")

    # ---------------- Create new embeddings ----------------
    logger.info("Splitting product data into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    documents: List[Document] = []
    for product in products:
        content = f"{product['name']}\n{product['description']}"
        chunks = text_splitter.split_text(content)
        for idx, chunk in enumerate(chunks):
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={"product_id": product["product_id"], "chunk_index": idx},
                )
            )

    logger.info(f"Generated {len(documents)} chunks for embedding.")

    logger.info("Storing embeddings in PGVector...")
    vector_store = PGVector.from_documents(
        documents=documents,
        embedding=embeddings,
        connection_string=db_url,
        collection_name=collection_name,
    )

    logger.info("Embeddings successfully stored in PGVector.")
    return vector_store


if __name__ == "__main__":
    logger.info("Loading products to embed...")
    products = load_products()
    embed_and_store(products)
