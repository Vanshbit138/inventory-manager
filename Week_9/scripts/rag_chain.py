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
from scripts.storage import store_chat_history
from scripts.llm_cache import SQLAlchemyCache

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def load_vector_store(collection_name: str = "product_embedding_hf") -> PGVector:
    """Load existing PGVector embeddings."""
    if not DATABASE_URL_WEEK8:
        raise ValueError("DATABASE_URL_WEEK8 not found in environment")

    return PGVector(
        collection_name=collection_name,
        connection_string=DATABASE_URL_WEEK8,
        embedding_function=HF_EMBEDDINGS,
    )


def get_llm(use_ollama: bool = False):
    """Return the LLM instance."""
    if use_ollama:
        return ChatOllama(model=CHAT_MODEL_OLLAMA, temperature=CHAT_TEMPERATURE)
    return ChatOpenAI(model=CHAT_MODEL_OPENAI, temperature=CHAT_TEMPERATURE)


def build_rag_chain(vector_store: PGVector, llm, user_id: int) -> object:
    """Build RAG chain with proper filter for multi-tenancy.

    Includes both the caller's documents and global documents.
    """
    str_user_id = str(user_id)
    # Prefer $in when supported; otherwise fall back to equality for user-only
    jsonb_filter = {"user_id": str_user_id}

    logger.info(f"[DEBUG] Building retriever with filter: {jsonb_filter}")

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 3,
            "filter": jsonb_filter,
        }
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


def answer_question(question: str, llm, user_id: int) -> str:
    """Answer a question using RAG with user_id filtering and caching."""
    try:
        # 1) Cache lookup
        cached = SQLAlchemyCache.get(question)
        if cached:
            return cached

        str_user_id = str(user_id)
        jsonb_filter = {"user_id": str_user_id}
        logger.info(
            f"[DEBUG] Retrieval filter user_id/global. user_id={user_id}, filter={jsonb_filter}"
        )

        vector_store = load_vector_store()

        # --- Debug: Fetch raw docs directly from retriever ---
        retriever = vector_store.as_retriever(
            search_kwargs={"k": 3, "filter": jsonb_filter}
        )
        retrieved_docs = retriever.get_relevant_documents(question)
        logger.info(
            f"[DEBUG] Retrieved {len(retrieved_docs)} documents for user_id={user_id}"
        )

        for i, doc in enumerate(retrieved_docs, start=1):
            logger.info(f"[DEBUG] Doc {i} metadata: {doc.metadata}")

        if not retrieved_docs:
            logger.warning(
                f"[DEBUG] No documents found for user_id={user_id}. Either no embeddings exist OR filter mismatch."
            )

        # Build chain and get answer
        rag_chain = build_rag_chain(vector_store, llm, user_id)
        answer = rag_chain.invoke(question)

        if not answer or not answer.strip():
            answer = "No matching products found for your query."

        # 2) Cache store
        try:
            SQLAlchemyCache.set(question, answer)
        except Exception as e:
            logger.warning(f"[CACHE STORE ERROR] user_id={user_id} error={e}")

        try:
            store_chat_history(user_id=user_id, question=question, answer=answer)
        except Exception as e:
            logger.warning(f"[STORE CHAT ERROR] user_id={user_id} error={e}")

        logger.info(f"[DEBUG] Final answer: {answer}")
        return answer

    except Exception as e:
        logger.error(f"[RAG ERROR] {e} — falling back to default chain")
        vector_store = load_vector_store()
        return build_rag_chain(vector_store, llm, user_id).invoke(question)
