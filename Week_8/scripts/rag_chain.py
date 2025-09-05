# scripts/rag_chain.py
"""
RAG pipeline using your existing product_embeddings table.
1. Load embeddings from PGVector.
2. Retrieve relevant product chunks.
3. Pass context + question to ChatOpenAI.
4. Generate answer.
"""

import logging
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.schema import StrOutputParser

from constants import CHAT_MODEL, CHAT_TEMPERATURE, EMBEDDING_MODEL

# ---------------- Setup ----------------
load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in environment or .env")


def load_vector_store(collection_name: str = "product_embeddings") -> PGVector:
    """
    Load existing PGVector embeddings from the database.
    """
    db_url = os.getenv("DATABASE_URL_WEEK8")
    if not db_url:
        raise ValueError("DATABASE_URL_WEEK8 not found in environment variables")

    logger.info(f"Loading vector store from collection '{collection_name}'...")
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)

    vector_store = PGVector(
        collection_name=collection_name,
        connection_string=db_url,
        embedding_function=embeddings,  # Required for similarity search
    )
    return vector_store


def build_rag_chain(vector_store: PGVector):
    """
    Build a simple RAG pipeline: retriever → prompt → LLM → output parser
    """
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Use the provided product context to answer the user's question.",
            ),
            ("human", "Context:\n{context}\n\nQuestion: {question}"),
        ]
    )

    llm = ChatOpenAI(model=CHAT_MODEL, temperature=CHAT_TEMPERATURE)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


def main():
    logger.info("Loading existing embeddings from vector DB...")
    vector_store = load_vector_store()

    logger.info("Building RAG chain...")
    rag_chain = build_rag_chain(vector_store)

    # Loop for user input
    while True:
        question = input("\nAsk a question about products (or 'exit'): ")
        if question.lower() in {"exit", "quit"}:
            break

        # Retrieve relevant documents
        docs = vector_store.as_retriever().invoke(question)
        if docs:
            print("\n[DEBUG] Retrieved Chunks:")
            for d in docs:
                print("-", d.page_content)
        else:
            print("\n[DEBUG] No chunks retrieved.")

        # Run RAG chain
        answer = rag_chain.invoke(question)
        print("\nA:", answer)


if __name__ == "__main__":
    main()
