"""
Shared Qdrant client.

Creates the prompt cache collection if it does not already exist.
Every service should import this client instead of creating
its own Qdrant connection.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from core.config import settings
from core.logging import logger


client = QdrantClient(
    host=settings.QDRANT_HOST,
    port=settings.QDRANT_PORT,
)

COLLECTION_NAME = settings.QDRANT_COLLECTION


try:
    collections = client.get_collections()

    existing = [
        collection.name
        for collection in collections.collections
    ]

    if COLLECTION_NAME not in existing:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )

        logger.info(
            "Created Qdrant collection",
            collection=COLLECTION_NAME,
        )

    else:

        logger.info(
            "Qdrant collection already exists",
            collection=COLLECTION_NAME,
        )

except Exception as e:

    logger.error(
        "Failed to initialize Qdrant",
        error=str(e),
    )

    raise