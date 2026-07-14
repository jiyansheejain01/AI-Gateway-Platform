"""
Shared Qdrant client.

Creates the prompt cache collection if it does not already exist.
Every service should import this client instead of creating
its own Qdrant connection.
"""
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from core.config import settings
from core.logging import logger


if settings.LOCAL_MODE:

    client = QdrantClient(
        path=settings.QDRANT_PATH
    )

    logger.info("Using Embedded Qdrant (LOCAL_MODE)")

else:

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
"""

#============================================================================
"""
Shared Qdrant client.
TEMPORARY DEBUG VERSION
"""

from qdrant_client import QdrantClient

from core.config import settings
from core.logging import logger

print("QDRANT STEP 1")

if settings.LOCAL_MODE:
    client = QdrantClient(path=settings.QDRANT_PATH)
    logger.info("Using Embedded Qdrant (LOCAL_MODE)")
else:
    client = QdrantClient(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT,
    )
    logger.info("Using Remote Qdrant")

print("QDRANT STEP 2")

# TEMPORARILY DISABLE COLLECTION INITIALIZATION
# COMMENTED FOR DEBUGGING
#
# from qdrant_client.models import Distance, VectorParams
#
# COLLECTION_NAME = settings.QDRANT_COLLECTION
#
# collections = client.get_collections()
#
# existing = [
#     collection.name
#     for collection in collections.collections
# ]
#
# if COLLECTION_NAME not in existing:
#     client.create_collection(
#         collection_name=COLLECTION_NAME,
#         vectors_config=VectorParams(
#             size=384,
#             distance=Distance.COSINE,
#         ),
#     )
#
# logger.info("Qdrant initialized")

print("QDRANT STEP 3")