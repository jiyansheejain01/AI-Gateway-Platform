"""
Llama model client using Ollama.
"""

from ollama import chat

from core.config import settings
from core.logging import logger


def generate(messages: list) -> dict:
    """
    Generate a response using the configured Llama model.
    """

    logger.info(
        "Calling Llama model",
        model=settings.LLAMA_MODEL,
    )

    response = chat(
        model=settings.LLAMA_MODEL,
        messages=messages,
    )

    return {
        "model": settings.LLAMA_MODEL,
        "response": response["message"]["content"],
    }