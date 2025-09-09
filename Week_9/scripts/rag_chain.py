import logging
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.schema import StrOutputParser

from scripts.constants import CHAT_MODEL, CHAT_TEMPERATURE
from prompts.system_prompt import SYSTEM_PROMPT
from scripts.llm_cache import SQLAlchemyCache

# ---------------- Setup ----------------
load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def load_vector_store(collection_name: str = "product_embeddings_hf") -> PGVector:
    """Load existing PGVector embeddings (HuggingFace) from the database."""
    db_url = os.getenv("DATABASE_URL_WEEK8")
    if not db_url:
        raise ValueError("DATABASE_URL_WEEK8 not found in environment variables")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = PGVector(
        collection_name=collection_name,
        connection_string=db_url,
        embedding_function=embeddings,
    )
    return vector_store


def build_rag_chain(vector_store: PGVector):
    """Build a simple RAG pipeline: retriever → prompt → LLM → output parser"""
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
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


# Initialize globally (Flask can reuse this)
_vector_store = load_vector_store()
_rag_chain = build_rag_chain(_vector_store)


def answer_question(question: str) -> str:
    """
    Return answer from cache if available, otherwise generate via RAG chain.
    Skips cache if Flask app context is not available (for CLI testing).
    """
    try:
        cached_answer = SQLAlchemyCache.get(question)
        if cached_answer:
            logger.info(f"[CACHE HIT] Question found in cache: {question}")
            return cached_answer
    except RuntimeError:
        # Flask app context not available → skip cache
        logger.info(
            f"[CACHE SKIP] Running outside Flask context for question: {question}"
        )

    answer = _rag_chain.invoke(question)

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
        print("A:", answer_question(q))
