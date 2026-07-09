"""
LLM Orchestrator.
Routes requests to the selected model.
"""

from core.logging import logger

from services.llm_service.llama import generate as llama_generate
from services.llm_service.phi import generate as phi3_generate


def generate_response(model: str, messages: list) -> dict:
    """
    Route the request to the appropriate LLM provider.
    """

    logger.info(
        "Routing request to LLM",
        model=model,
    )

    if model == "phi3":
        return phi3_generate(messages)

    if model == "llama":
        return llama_generate(messages)

    logger.error(
        "Unknown model requested",
        model=model,
    )

    raise ValueError(f"Unknown model: {model}")