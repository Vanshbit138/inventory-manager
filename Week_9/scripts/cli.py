# scripts/cli.py
"""
Command-line interface for GPT queries.
"""

import logging
from query_gpt import get_embedding, ask_gpt
from storage import store_query


def cli_loop() -> None:
    """Run the interactive CLI loop."""
    print("=== GPT CLI (LangChain-powered) (type 'exit' to quit) ===\n")
    while True:
        question = input("Enter your question: ").strip()
        if not question:
            print(" Empty input. Please enter a valid question.")
            continue

        if question.lower() == "exit":
            print("Exiting CLI. Goodbye!")
            break

        fs = input("Use few-shot example? (y/n): ").lower() == "y"

        # Store embedding
        embedding = get_embedding(question)
        if embedding:
            store_query(question, embedding)

        # Get GPT answer
        answer = ask_gpt(question, few_shot_example=fs)
        print("\nAnswer:\n", answer)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )
    cli_loop()
