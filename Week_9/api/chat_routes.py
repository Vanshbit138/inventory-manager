# Week_6_and_7/api/chat_routes.py

from flask import Blueprint, request, jsonify
from scripts.rag_chain import answer_question

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


@chat_bp.route("/inventory", methods=["POST"])
def chat_inventory() -> tuple:
    """Chat with inventory using RAG (OpenAI or Ollama)."""
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question' in request body"}), 400

    question = data["question"]
    use_ollama = data.get("use_ollama", False)  # default → OpenAI

    answer = answer_question(question, use_ollama=use_ollama)

    model_used = "ollama-llama3" if use_ollama else "openai-gpt-4o-mini"

    return (
        jsonify({"question": question, "answer": answer, "model_used": model_used}),
        200,
    )
