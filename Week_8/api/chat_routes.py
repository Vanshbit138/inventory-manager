# api/chat_routes.py
from flask import Blueprint, request, jsonify
from scripts.rag_chain import answer_question

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


@chat_bp.route("/inventory", methods=["POST"])
def chat_inventory():
    """Chat endpoint: takes a question, returns an LLM-generated answer."""
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question' field in request body"}), 400

    question = data["question"]
    try:
        answer = answer_question(question)
        return jsonify({"question": question, "answer": answer}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
