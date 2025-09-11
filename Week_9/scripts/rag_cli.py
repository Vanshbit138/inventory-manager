# scripts/rag_cli.py
"""
Command-line interface for testing the RAG pipeline with OpenAI or Ollama.
"""
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.rag_chain import answer_question, get_llm


def rag_cli_loop() -> None:
    """Run the interactive CLI loop for RAG testing."""
    print("=== RAG CLI (OpenAI / Ollama) ===")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Ask a question: ").strip()
        if not question:
            print(" Empty input. Please enter a valid question.")
            continue

        if question.lower() in {"exit", "quit"}:
            print("Exiting RAG CLI. Goodbye!")
            break

        use_ollama = input("Use Ollama? (y/n): ").lower() == "y"
        llm = get_llm(use_ollama=use_ollama)
        answer = answer_question(question, llm)
        print("\nAnswer:\n", answer, "\n")


if __name__ == "__main__":
    rag_cli_loop()
