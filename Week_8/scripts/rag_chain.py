# scripts/rag_chain.py

import logging
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.schema import StrOutputParser

from scripts.constants import CHAT_MODEL, CHAT_TEMPERATURE, EMBEDDING_MODEL
from prompts.system_prompt import SYSTEM_PROMPT

# ---------------- Setup ----------------
load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in environment or .env")


def load_vector_store(collection_name: str = "product_embeddings") -> PGVector:
    """Load existing PGVector embeddings from the database."""
    db_url = os.getenv("DATABASE_URL_WEEK8")
    if not db_url:
        raise ValueError("DATABASE_URL_WEEK8 not found in environment variables")

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)

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
            ("system", SYSTEM_PROMPT),  # Use system prompt from file
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
    """Public function Flask will call to answer user queries."""
    return _rag_chain.invoke(question)


# For CLI testing
if __name__ == "__main__":
    while True:
        q = input("Ask a question (or 'exit'): ")
        if q.lower() in {"exit", "quit"}:
            break
        print("A:", answer_question(q))
