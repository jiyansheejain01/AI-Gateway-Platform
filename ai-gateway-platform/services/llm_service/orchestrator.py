"""
LLM Orchestrator.
Routes requests to the selected model.
"""

from core.logging import logger

from services.llm_service.groq_client import generate as groq_generate


def generate_response(model: str, messages: list) -> dict:
    """
    For now route every request to Groq.
    """

    logger.info(
        "Routing request to Groq",
        requested_model=model,
    )

    return groq_generate(messages)