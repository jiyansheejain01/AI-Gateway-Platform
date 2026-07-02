"""
Integration with Qdrant vector database for storing and querying vector embeddings.
"""
from qdrant_client.models import Distance, VectorParams
from services.cache_service.qdrant_client import client

COLLECTION_NAME = "prompt_cache"

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
            distance=Distance.COSINE
        )
    )

    print("Qdrant collection created.")

else:

    print("Qdrant collection already exists.")