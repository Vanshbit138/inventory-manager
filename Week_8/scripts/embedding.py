# scripts/ingest_embeddings.py
"""
Generate embeddings for product data and store them in PGVector.
This version aligns with the RAG chain and project structure.
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


def embed_and_store(products: List[Dict]) -> PGVector:
    """
    Generate embeddings for product data and store them in PGVector.
    """
    db_url = os.getenv("DATABASE_URL_WEEK8")
    if not db_url:
        raise ValueError("DATABASE_URL_WEEK8 not found in environment variables")

    logger.info("Initializing OpenAI embeddings...")
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    logger.info("Splitting product data into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
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
        collection_name="product_embeddings",
    )

    logger.info("Embeddings successfully stored in PGVector.")
    return vector_store


if __name__ == "__main__":
    logger.info("Loading products to embed...")
    products = load_products()
    embed_and_store(products)
