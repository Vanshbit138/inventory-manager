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


def build_rag_chain(vector_store: PGVector, llm) -> object:
    """Build a RAG pipeline with the specified LLM."""
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

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


# Initialize vector store globally (default → OpenAI)
_vector_store = load_vector_store()


def answer_question(question: str, llm) -> str:
    """Answer from cache if available, else generate via RAG chain (OpenAI or Ollama)."""
    try:
        from scripts.llm_cache import SQLAlchemyCache
    except ImportError:
        SQLAlchemyCache = None

    # Single try/except for cache operations
    try:
        if SQLAlchemyCache:
            cached_answer = SQLAlchemyCache.get(question)
            if cached_answer:
                logger.info(f"[CACHE HIT] Question found in cache: {question}")
                return cached_answer

        # Otherwise fetch new answer
        rag_chain = build_rag_chain(_vector_store, llm)
        answer = rag_chain.invoke(question)

        if SQLAlchemyCache:
            SQLAlchemyCache.set(question, answer)
            logger.info(f"[CACHE SET] Storing answer for question: {question}")

        return answer

    except Exception as e:
        logger.warning(f"[CACHE ERROR] {e} — proceeding without cache")
        rag_chain = build_rag_chain(_vector_store, llm)
        return rag_chain.invoke(question)
