from services.cache_service.semantic_cache import (
    store_embedding,
    search_similar_prompt
)

print("Storing embedding...")

store_embedding(
    "What is Artificial Intelligence?",
    {
        "answer": "Artificial Intelligence is..."
    }
)

print("Searching...")

result = search_similar_prompt(
    "Explain AI"
)

print(result)