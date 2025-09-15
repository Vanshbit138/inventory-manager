import logging
import os
import sys
import re

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

FALLBACK = "I can only answer questions about your inventory and your uploaded documents. Please ask about those topics."
BOILERPLATE_PATTERNS = [
    r"^\s*based on (the )?(provided|available)?\s*context[:,]?\s*",
    r"^\s*based on (the )?(available )?documents[:,]?\s*",
    r"^\s*according to (the )?(context|documents)[:,]?\s*",
    r"^\s*from (the )?(context|documents)[:,]?\s*",
]


def clean_answer(text: str) -> str:
    t = text or ""
    for pat in BOILERPLATE_PATTERNS:
        t = re.sub(pat, "", t, flags=re.IGNORECASE)
    t = re.sub(r"^\s*(it (appears|seems) that[:,]?\s*)", "", t, flags=re.IGNORECASE)
    return t.strip()


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
    """Build RAG chain with multi-tenant filter and similarity threshold."""
    str_user_id = str(user_id)
    jsonb_filter = {"user_id": str_user_id}

    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 3,
            "filter": jsonb_filter,
            "score_threshold": 0.30,  # tune 0.2–0.4 as needed
        },
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
    """Answer using RAG with user_id filtering, threshold fallback, and tenant-safe cache."""
    try:
        # Tenant-safe cache key to avoid cross-tenant leakage
        normalized_q = (question or "").strip().lower()
        cache_key = f"{user_id}::{normalized_q}"

        cached = SQLAlchemyCache.get(cache_key)
        if cached:
            return cached

        str_user_id = str(user_id)
        jsonb_filter = {"user_id": str_user_id}
        vector_store = load_vector_store()

        # Probe with same threshold to detect irrelevance
        probe_retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 3, "filter": jsonb_filter, "score_threshold": 0.30},
        )
        retrieved_docs = probe_retriever.get_relevant_documents(question)

        if not retrieved_docs:
            SQLAlchemyCache.set(cache_key, FALLBACK)
            return FALLBACK

        rag_chain = build_rag_chain(vector_store, llm, user_id)
        answer = rag_chain.invoke(question)
        answer = clean_answer(answer)

        if not answer or not answer.strip():
            answer = FALLBACK

        try:
            SQLAlchemyCache.set(cache_key, answer)
        except Exception as e:
            logger.warning(f"[CACHE STORE ERROR] user_id={user_id} error={e}")

        try:
            store_chat_history(user_id=user_id, question=question, answer=answer)
        except Exception as e:
            logger.warning(f"[STORE CHAT ERROR] user_id={user_id} error={e}")

        return answer

    except Exception as e:
        logger.error(f"[RAG ERROR] {e}")
        return FALLBACK
