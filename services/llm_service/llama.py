"""
Llama model client using Ollama.
"""

from ollama import chat


def generate(messages: list) -> dict:
    """
    Send the entire conversation history
    to the local Llama model.
    """

    response = chat(
        model="llama3:latest",
        messages=messages
    )

    return {
        "model": "llama3",
        "response": response["message"]["content"]
    }