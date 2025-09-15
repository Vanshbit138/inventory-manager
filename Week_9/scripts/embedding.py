# scripts/embedding.py
"""
Multi-tenant embeddings writer.
Usage:
  python scripts/embedding.py --user_id 17 --collection product_embedding_hf
"""

import argparse
import logging
import os
from typing import List, Dict
from dotenv import load_dotenv

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.documents import Document

from data_loader import load_products  # Updated to fetch products per user
from constants import CHUNK_SIZE, CHUNK_OVERLAP

# ---------------- Setup ----------------
load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


def embed_and_store(
    products: List[Dict],
    collection_name: str,
    user_id: int,
) -> PGVector:
    """
    Embeds products for a specific user_id and stores them in a PGVector collection.
    Skips already embedded products for that user.
    """
    db_url = os.getenv("DATABASE_URL_WEEK8")
    if not db_url:
        raise ValueError("DATABASE_URL_WEEK8 not found in environment")

    logger.info("Using database: %s", db_url)

    # Initialize embeddings and vector store
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_store = PGVector(
        collection_name=collection_name,
        connection_string=db_url,
        embedding_function=embeddings,
    )

    # Fetch existing embeddings for this user
    try:
        existing_docs = vector_store.similarity_search(
            query="placeholder",
            k=1000,
            filter={"user_id": str(user_id)},  # Ensure string match
        )
    except Exception as e:
        logger.warning("Could not fetch existing docs for user_id=%s: %s", user_id, e)
        existing_docs = []

    existing_product_ids = {
        str(d.metadata.get("product_id")) for d in existing_docs if d.metadata
    }
    logger.info(
        "Found %d existing product_ids for user_id=%s",
        len(existing_product_ids),
        user_id,
    )

    # Filter products not yet embedded
    new_products = [
        p for p in products if str(p["product_id"]) not in existing_product_ids
    ]
    if not new_products:
        logger.info("No new products to embed for user_id=%s", user_id)
        return vector_store

    logger.info("Found %d new products to embed", len(new_products))

    # Split text into chunks and create Document objects
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    documents = []
    for product in new_products:
        content = f"{product['name']}\n{product['description']}"
        chunks = text_splitter.split_text(content)
        for idx, chunk in enumerate(chunks):
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "product_id": str(product["product_id"]),
                        "chunk_index": idx,
                        "user_id": str(user_id),  # Multi-tenancy enforced
                    },
                )
            )

    logger.info(
        "Preparing %d document chunks for user_id=%s into collection '%s'",
        len(documents),
        user_id,
        collection_name,
    )

    # Store embeddings
    try:
        vector_store.add_documents(documents)
        logger.info(
            "Successfully stored %d chunks in '%s'", len(documents), collection_name
        )
    except Exception as e:
        logger.error("Failed to store documents: %s", e)
        raise

    return vector_store


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--user_id", type=int, required=True, help="User ID for multi-tenant embeddings"
    )
    parser.add_argument(
        "--collection", type=str, default="product_embedding_hf", help="Collection name"
    )
    args = parser.parse_args()

    logger.info("Loading products for embedding...")
    products = load_products(
        user_id=args.user_id
    )  # Pass user_id to fetch only user's products

    if not products:
        logger.warning("No products found to embed. Exiting.")
    else:
        embed_and_store(products, collection_name=args.collection, user_id=args.user_id)
