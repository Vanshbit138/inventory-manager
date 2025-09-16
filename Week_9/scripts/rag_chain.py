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

# Intent patterns
GREETING_RE = re.compile(
    r"^\s*(hi|hello|hey|good (morning|afternoon|evening)|greetings|how (can|may) (you|u) help|how can you assist|how do you help)\b",
    re.IGNORECASE,
)
FAREWELL_RE = re.compile(
    r"\b(bye|goodbye|see you|see ya|take care|later)\b",
    re.IGNORECASE,
)
THANKS_RE = re.compile(
    r"\b(thanks|thank you|appreciate it|much appreciated)\b",
    re.IGNORECASE,
)
EMOTION_RE = re.compile(
    r"\b(i\s*(am|'m)\s*(angry|mad|upset|frustrated|annoyed|sad|down|depressed|anxious|stressed|worried|overwhelmed|happy|glad|excited|joyful))\b",
    re.IGNORECASE,
)


def clean_answer(text: str) -> str:
    t = text or ""
    for pat in BOILERPLATE_PATTERNS:
        t = re.sub(pat, "", t, flags=re.IGNORECASE)
    t = re.sub(r"^\s*(it (appears|seems) that[:,]?\s*)", "", t, flags=re.IGNORECASE)
    return t.strip()


def is_greeting(q: str) -> bool:
    return bool(GREETING_RE.search(q or ""))


def is_farewell(q: str) -> bool:
    return bool(FAREWELL_RE.search(q or ""))


def is_thanks(q: str) -> bool:
    return bool(THANKS_RE.search(q or ""))


def is_emotion(q: str) -> bool:
    return bool(EMOTION_RE.search(q or ""))


def greeting_response(q: str) -> str:
    if re.search(r"afternoon", q or "", re.IGNORECASE):
        prefix = "Good afternoon!"
    elif re.search(r"morning", q or "", re.IGNORECASE):
        prefix = "Good morning!"
    elif re.search(r"evening", q or "", re.IGNORECASE):
        prefix = "Good evening!"
    else:
        prefix = "Hello!"
    return f"{prefix} I can help you query your inventory and your uploaded documents. Ask about products, prices, stock, or the content of your documents."


def farewell_response(q: str) -> str:
    return "Goodbye! Take care, and feel free to reach out anytime you need help."


def thanks_response(q: str) -> str:
    return "You're welcome! If you need anything else, I'm here to help."


def emotion_response(q: str) -> str:
    m = EMOTION_RE.search(q or "")
    tone = (m.group(3).lower() if m else "").strip()
    if tone in {"angry", "mad", "upset", "frustrated", "annoyed"}:
        return "I'm sorry you're feeling this way. If you'd like, tell me what's causing the frustration, and I can try to help or offer suggestions."
    if tone in {"sad", "down", "depressed"}:
        return "I'm sorry you're feeling sad. You're not alone—I'm here to listen and help. Would you like to talk about what's on your mind?"
    if tone in {"anxious", "stressed", "worried", "overwhelmed"}:
        return "That sounds stressful. Taking a deep breath can help. If you want, share a bit more and I can offer ideas or support."
    if tone in {"happy", "glad", "excited", "joyful"}:
        return "That's great to hear! I'm happy for you. If there's anything you'd like to explore or get done while you're in a good mood, I'm here to help."
    return "Thanks for sharing how you feel. I'm here to support you—would you like to tell me more so I can help?"


def load_vector_store(collection_name: str = "product_embedding_hf") -> PGVector:
    if not DATABASE_URL_WEEK8:
        raise ValueError("DATABASE_URL_WEEK8 not found in environment")
    return PGVector(
        collection_name=collection_name,
        connection_string=DATABASE_URL_WEEK8,
        embedding_function=HF_EMBEDDINGS,
    )


def get_llm(use_ollama: bool = False):
    if use_ollama:
        return ChatOllama(model=CHAT_MODEL_OLLAMA, temperature=CHAT_TEMPERATURE)
    return ChatOpenAI(model=CHAT_MODEL_OPENAI, temperature=CHAT_TEMPERATURE)


def build_rag_chain(vector_store: PGVector, llm, user_id: int) -> object:
    str_user_id = str(user_id)
    jsonb_filter = {"user_id": str_user_id}
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 3, "filter": jsonb_filter, "score_threshold": 0.30},
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
    try:
        normalized_q = (question or "").strip().lower()
        cache_key = f"{user_id}::{normalized_q}"

        # Handle small-talk intents without requiring context
        if is_greeting(question):
            resp = greeting_response(question)
            try:
                SQLAlchemyCache.set(cache_key, resp)
            except Exception:
                pass
            return resp
        if is_thanks(question):
            resp = thanks_response(question)
            try:
                SQLAlchemyCache.set(cache_key, resp)
            except Exception:
                pass
            return resp
        if is_farewell(question):
            resp = farewell_response(question)
            try:
                SQLAlchemyCache.set(cache_key, resp)
            except Exception:
                pass
            return resp
        if is_emotion(question):
            resp = emotion_response(question)
            try:
                SQLAlchemyCache.set(cache_key, resp)
            except Exception:
                pass
            return resp

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
