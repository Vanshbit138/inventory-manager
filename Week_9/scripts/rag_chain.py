import logging
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from dotenv import load_dotenv
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.schema import StrOutputParser

from scripts.constants import (
    HF_EMBEDDINGS,
    DATABASE_URL_WEEK8,
    OPENAI_LLM,
    OLLAMA_LLM,
)
from prompts.system_prompt import SYSTEM_PROMPT

# ---------------- Setup ----------------
load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def load_vector_store(collection_name: str = "product_embeddings_hf") -> PGVector:
    """Load existing PGVector embeddings (HuggingFace) from the database."""
    if not DATABASE_URL_WEEK8:
        raise ValueError("DATABASE_URL_WEEK8 not found in environment variables")

    return PGVector(
        collection_name=collection_name,
        connection_string=DATABASE_URL_WEEK8,
        embedding_function=HF_EMBEDDINGS,
    )


def build_rag_chain(vector_store: PGVector, use_ollama: bool = False):
    """Build a RAG pipeline with either OpenAI or Ollama LLM."""
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "Context:\n{context}\n\nQuestion: {question}"),
        ]
    )

    llm = OLLAMA_LLM if use_ollama else OPENAI_LLM

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


# Initialize globally (default → OpenAI)
_vector_store = load_vector_store()
_rag_chain = build_rag_chain(_vector_store, use_ollama=False)


def answer_question(question: str, use_ollama: bool = False) -> str:
    """Answer from cache if available, else generate via RAG chain (OpenAI or Ollama)."""

    #  Import here to avoid circular import
    try:
        from scripts.llm_cache import SQLAlchemyCache
    except ImportError:
        SQLAlchemyCache = None

    # Try cache
    if SQLAlchemyCache:
        try:
            cached_answer = SQLAlchemyCache.get(question)
            if cached_answer:
                logger.info(f"[CACHE HIT] Question found in cache: {question}")
                return cached_answer
        except RuntimeError:
            logger.info(
                f"[CACHE SKIP] Running outside Flask context for question: {question}"
            )

    # Otherwise, get fresh answer
    rag_chain = build_rag_chain(_vector_store, use_ollama=use_ollama)
    answer = rag_chain.invoke(question)

    # Save to cache
    if SQLAlchemyCache:
        try:
            SQLAlchemyCache.set(question, answer)
            logger.info(f"[CACHE SET] Storing answer for question: {question}")
        except RuntimeError:
            logger.info(
                f"[CACHE SKIP] Could not store cache outside Flask context for question: {question}"
            )

    return answer


# For CLI testing
if __name__ == "__main__":
    while True:
        q = input("Ask a question (or 'exit'): ")
        if q.lower() in {"exit", "quit"}:
            break
        mode = input("Use Ollama? (y/n): ").lower() == "y"
        print("A:", answer_question(q, use_ollama=mode))
