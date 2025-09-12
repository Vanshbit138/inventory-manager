# api/chat_routes.py
from flask import Blueprint, request, jsonify
from scripts.rag_chain import answer_question, get_llm
from .security.decorators import jwt_required, roles_required, get_current_user_id

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


@chat_bp.route("/inventory", methods=["POST"])
@jwt_required
@roles_required("admin", "manager")  # Only admin & manager can access
def chat_inventory() -> tuple:
    """Chat with inventory using RAG (OpenAI or Ollama)."""
    data = request.get_json() or {}
    question = (data.get("question") or "").strip()
    if not question:
        return jsonify({"error": "Missing 'question' in request body"}), 400

    use_ollama = data.get("use_ollama", False)

    try:
        user_id = get_current_user_id()
    except Exception as e:
        return jsonify({"error": "Unauthorized: invalid token", "details": str(e)}), 401

    llm = get_llm(use_ollama=use_ollama)
    answer = answer_question(question, llm, user_id=user_id)

    model_used = "ollama-llama3" if use_ollama else "openai-gpt-4o-mini"

    return (
        jsonify(
            {
                "user_id": user_id,
                "question": question,
                "answer": answer,
                "model_used": model_used,
            }
        ),
        200,
    )
