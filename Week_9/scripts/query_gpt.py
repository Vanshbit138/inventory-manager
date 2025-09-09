# scripts/query_service.py
"""
LangChain GPT query service.

Responsibilities:
- Generate embeddings using OpenAI.
- Query GPT using LangChain (zero-shot and few-shot).
- Log token usage and approximate cost.

SOLID Principles:
- SRP: Embedding generation and GPT query kept separate.
- OCP: Easy to extend with new prompts or models without modifying existing logic.
"""

import os
import logging
from typing import List

from dotenv import load_dotenv

load_dotenv()
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

from constants import EMBEDDING_MODEL, CHAT_MODEL, CHAT_TEMPERATURE, TOKEN_COST_PER_1K

# ------------------ Environment ------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set in environment or .env")

# OpenAI client (raw usage + embeddings)
client = OpenAI(api_key=OPENAI_API_KEY)

# LangChain chat model
chat_model = ChatOpenAI(
    model=CHAT_MODEL,
    temperature=CHAT_TEMPERATURE,
    api_key=OPENAI_API_KEY,
)
parser = StrOutputParser()

# ------------------ Prompts ------------------
default_prompt = ChatPromptTemplate.from_messages([("user", "{question}")])

few_shot_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        (
            "user",
            "Translate the following English sentences to French:\n"
            "Hello -> Bonjour\nGood morning -> Bonjour",
        ),
        ("user", "{question}"),
    ]
)


# ------------------ Core Functions ------------------
def get_embedding(text: str) -> List[float]:
    """
    Generate an embedding for a given text using OpenAI.

    Args:
        text (str): Input text.

    Returns:
        List[float]: Embedding vector.
    """
    try:
        resp = client.embeddings.create(model=EMBEDDING_MODEL, input=[text])
        return resp.data[0].embedding
    except Exception as e:
        logging.error("Failed to generate embedding: %s", str(e))
        return []


def ask_gpt(question: str, few_shot_example: bool = False) -> str:
    """
    Ask GPT a question using LangChain and return the answer.
    Also logs tokens used and approximate cost.

    Args:
        question (str): The user question.
        few_shot_example (bool): Whether to use few-shot prompting.

    Returns:
        str: GPT response text.
    """
    if not question.strip():
        logging.warning("Empty or whitespace-only question ignored.")
        return "Error: Question cannot be empty."

    try:
        # Use LangChain for structured response
        prompt = few_shot_prompt if few_shot_example else default_prompt
        chain = prompt | chat_model | parser
        answer = chain.invoke({"question": question})

        # Direct OpenAI call (for usage tracking)
        usage_resp = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[{"role": "user", "content": question}],
            max_tokens=200,
        )
        tokens_used = usage_resp.usage.total_tokens
        approx_cost = (tokens_used / 1000) * TOKEN_COST_PER_1K

        logging.info("Tokens used: %d", tokens_used)
        logging.info("Approx cost (USD): $%.6f", approx_cost)

        return answer

    except Exception as e:
        logging.error("GPT query failed: %s", str(e))
        return "Error: Could not get response from GPT."
