"""
Central place for constants such as model names, database URLs, etc.
API keys and secrets should remain in the .env file, not here.
"""

import os
from dotenv import load_dotenv

# Load environment variables
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Database URL (from .env)
DATABASE_URL = os.getenv("DATABASE_URL_WEEK8")

# Embedding and Chat Models
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"

# Cost estimation (tokens → USD) for reference
TOKEN_COST_PER_1K = 0.002
