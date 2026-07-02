"""
Semantic caching layer using embeddings to cache and retrieve responses with similar intent.
"""
import uuid

from qdrant_client.models import PointStruct

from services.embedding_service.embed import generate_embedding
from .qdrant_client import client

COLLECTION_NAME = "prompt_cache"


def store_embedding(
    prompt: str,
    response: dict
):
    """
    Store prompt embedding and its response in Qdrant.
    """

    embedding = generate_embedding(prompt)

    client.upsert(
        collection_name=COLLECTION_NAME,

        points=[
            PointStruct(
                id=str(uuid.uuid4()),

                vector=embedding,

                payload={
                    "prompt": prompt,
                    "response": response
                }
            )
        ]
    )

def search_similar_prompt(
    prompt: str,
    threshold: float = 0.75
):
    """
    Search for a semantically similar prompt.
    """

    embedding = generate_embedding(prompt)

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=embedding,
        limit=1
    )

    if not response.points:
        return None

    best_match = response.points[0]

    print(f"Similarity Score: {best_match.score:.4f}")

    if best_match.score >= threshold:
        return best_match.payload

    return None