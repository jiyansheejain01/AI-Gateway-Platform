"""
LLM Orchestrator.
Routes requests to the selected model.
"""

from services.llm_service.llama import generate as llama_generate
from services.llm_service.phi import generate as phi3_generate


def generate_response(model: str, messages: list):

    if model == "phi3":
        return phi3_generate(messages)

    elif model == "llama":
        return llama_generate(messages)

    else:
        raise ValueError(f"Unknown model: {model}")