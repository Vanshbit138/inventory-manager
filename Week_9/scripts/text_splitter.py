"""
Split product text into smaller chunks for embeddings.
"""

import logging
from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)


def chunk_products(
    products: List[Dict[str, str]], chunk_size: int = 200, chunk_overlap: int = 20
) -> List[Dict[str, str]]:
    """
    Convert product dicts into text chunks.

    Args:
        products (List[Dict]): List of products with product_id, name, description.
        chunk_size (int): Max characters per chunk.
        chunk_overlap (int): Overlap between chunks.

    Returns:
        List[Dict]: List of chunk dicts with product_id and text.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = []
    for product in products:
        text = f"Product Name: {product['name']}. Description: {product['description']}"
        product_chunks = splitter.split_text(text)
        for i, chunk in enumerate(product_chunks):
            chunks.append(
                {
                    "product_id": product["product_id"],  # ✅ FIXED
                    "chunk_index": i,
                    "text": chunk,
                }
            )

    logging.info("Created %d chunks from %d products", len(chunks), len(products))
    return chunks


if __name__ == "__main__":
    from db_loader import load_products

    products = load_products()
    chunks = chunk_products(products)
    for c in chunks[:5]:
        print(c)
