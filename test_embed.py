from services.embedding_service.embed import generate_embedding

embedding = generate_embedding(
    "What is Artificial Intelligence?"
)

print(f"Vector Length: {len(embedding)}")

print()

print(embedding[:10])