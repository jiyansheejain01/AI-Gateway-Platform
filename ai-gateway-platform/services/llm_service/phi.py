"""
Phi-3 model client using Ollama.
"""

from ollama import chat

from core.config import settings
from core.logging import logger


def generate(messages: list) -> dict:
    """
    Generate a response using the configured Phi-3 model.
    """

    logger.info(
        "Calling Phi-3 model",
        model=settings.PHI3_MODEL,
    )

    response = chat(
        model=settings.PHI3_MODEL,
        messages=messages,
    )

    return {
        "model": settings.PHI3_MODEL,
        "response": response["message"]["content"],
    }