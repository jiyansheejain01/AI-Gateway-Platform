"""
Phi-3 model client using Ollama.
"""

from ollama import chat


def generate(messages: list) -> dict:
    """
    Send the entire conversation history
    to the local Phi-3 model.
    """

    response = chat(
        model="phi3:latest",
        messages=messages
    )

    return {
        "model": "phi3",
        "response": response["message"]["content"]
    }