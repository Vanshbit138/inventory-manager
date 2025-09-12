# scripts/rag_chain.py
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
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from scripts.constants import (
    HF_EMBEDDINGS,
    DATABASE_URL_WEEK8,
    CHAT_MODEL_OPENAI,
    CHAT_MODEL_OLLAMA,
    CHAT_TEMPERATURE,
)
from prompts.system_prompt import SYSTEM_PROMPT
from scripts.storage import store_chat_history  # store the Q&A history

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


def get_llm(use_ollama: bool = False):
    """Return the appropriate LLM instance (OpenAI or Ollama)."""
    if use_ollama:
        return ChatOllama(model=CHAT_MODEL_OLLAMA, temperature=CHAT_TEMPERATURE)
    return ChatOpenAI(model=CHAT_MODEL_OPENAI, temperature=CHAT_TEMPERATURE)


def build_rag_chain(vector_store: PGVector, llm, user_id: int) -> object:
    """Build a RAG pipeline with the specified LLM, filtered by user_id."""
    # PGVector retriever supports metadata filtering; we rely on "user_id" in metadata
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3, "filters": {"user_id": user_id}}
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "Context:\n{context}\n\nQuestion: {question}"),
        ]
    )

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


# Initialize vector store globally
_vector_store = load_vector_store()


def answer_question(question: str, llm, user_id: int) -> str:
    """
    Answer using RAG and optionally a cache.
    This function is defensive about cache API differences and always tries to store chat history.
    """
    try:
        from scripts.llm_cache import SQLAlchemyCache
    except ImportError:
        SQLAlchemyCache = None

    try:
        # Try cache get with/without user_id (backwards compatibility)
        cached_answer = None
        if SQLAlchemyCache:
            try:
                cached_answer = SQLAlchemyCache.get(question, user_id=user_id)
            except TypeError:
                # older cache API might only accept 'question'
                cached_answer = SQLAlchemyCache.get(question)

        if cached_answer:
            logger.info(f"[CACHE HIT] user_id={user_id} Question found in cache")
            return cached_answer

        # Not cached → run chain
        rag_chain = build_rag_chain(_vector_store, llm, user_id)
        answer = rag_chain.invoke(question)

        # Try to set cache with both signatures
        if SQLAlchemyCache:
            try:
                SQLAlchemyCache.set(question, answer, user_id=user_id)
            except TypeError:
                SQLAlchemyCache.set(question, answer)

        # Store chat history (safe, non-blocking)
        try:
            store_chat_history(user_id=user_id, question=question, answer=answer)
        except Exception as e:
            logger.warning(f"[STORE CHAT ERROR] user_id={user_id} error={e}")

        return answer

    except Exception as e:
        logger.warning(f"[RAG ERROR] {e} — proceeding without cache")
        rag_chain = build_rag_chain(_vector_store, llm, user_id)
        return rag_chain.invoke(question)
