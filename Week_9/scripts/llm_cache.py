# scripts/llm_cache.py

from datetime import datetime
from api.models import LLMCache
from api.db import db
import logging

# ---------------- Setup Logging ----------------
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SQLAlchemyCache:
    """SQLAlchemy-based cache for LLM responses with TTL support."""

    ttl_seconds = 3600  # TTL in seconds

    @staticmethod
    def get(question: str):
        """Return cached answer if exists and not expired, else None"""
        cached = LLMCache.query.filter_by(question=question).first()
        if cached:
            if (
                cached.created_at
                and (datetime.utcnow() - cached.created_at).total_seconds()
                < SQLAlchemyCache.ttl_seconds
            ):
                logger.info(
                    f"[CACHE HIT] Returning cached answer for question: {question}"
                )
                return cached.answer
            else:
                # Expired, delete entry
                logger.info(f"[CACHE EXPIRED] Question expired in cache: {question}")
                db.session.delete(cached)
                db.session.commit()
        else:
            logger.info(f"[CACHE MISS] No cached answer for question: {question}")
        return None

    @staticmethod
    def set(question: str, answer: str):
        """Store question-answer in the cache"""
        logger.info(f"[CACHE SET] Storing answer for question: {question}")
        cache_entry = LLMCache(
            question=question, answer=answer, created_at=datetime.utcnow()
        )
        db.session.add(cache_entry)
        db.session.commit()
