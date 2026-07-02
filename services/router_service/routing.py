"""
Smart routing algorithms that direct traffic to the most optimal LLM based on cost, speed, or quality.
"""

from services.router_service.classifier import classify_prompt


def route_prompt(prompt: str) -> dict:
    result = classify_prompt(prompt)

    if result["category"] == "simple":
        model = "phi3"
    else:
        model = "llama"

    return {
        "model": model,
        "score": result["score"],
        "category": result["category"]
    }
