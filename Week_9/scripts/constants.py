"""
Central place for constants such as model names, database URLs, etc.
API keys and secrets should remain in the .env file, not here.
"""

import os
from dotenv import load_dotenv

# ---------------- Load environment ----------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# ---------------- Database ----------------
DATABASE_URL_WEEK8 = os.getenv("DATABASE_URL_WEEK8")

# ---------------- Models ----------------
# Embedding and Chat Models
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # HuggingFace model
CHAT_MODEL = "gpt-4o-mini"

# Temperature for GPT responses
CHAT_TEMPERATURE = 0.0

# Cost estimation (tokens → USD) for reference
TOKEN_COST_PER_1K = 0.002

# Database tables
PRODUCT_TABLE = "products"

# Text splitting config
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# ---------------- Embeddings ----------------
# HuggingFace Embeddings (default)
from langchain_huggingface import HuggingFaceEmbeddings


HF_EMBEDDINGS = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# If you want to switch to OpenAI later, uncomment below:
# from langchain_openai import OpenAIEmbeddings
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OPENAI_EMBEDDINGS = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)
