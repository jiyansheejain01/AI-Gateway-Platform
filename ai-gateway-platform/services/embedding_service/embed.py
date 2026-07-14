"""
Embedding Service

Uses Cohere Embeddings API instead of a local
SentenceTransformer model.

Benefits:
- No torch
- No transformers
- Very low RAM usage
- Suitable for Render free tier
"""

import cohere

from core.config import settings
from core.logging import logger


# ==========================================================
# Cohere Client
# ==========================================================

client = cohere.ClientV2(
    api_key=settings.COHERE_API_KEY,
)


# ==========================================================
# Embedding Generation
# ==========================================================

def generate_embedding(prompt: str) -> list[float]:
    """
    Generate an embedding vector using Cohere.
    """

    logger.info(
        "Generating embedding",
        provider="Cohere",
    )

    try:

        response = client.embed(
            texts=[prompt],
            model="embed-v4.0",
            input_type="search_query",
            embedding_types=["float"],
        )

        return response.embeddings.float_[0]

    except Exception as e:

        logger.error(
            "Embedding generation failed",
            error=str(e),
        )

        raise