"""
Service to generate embeddings using OpenAI, HuggingFace, or Cohere models.
"""

from sentence_transformers import SentenceTransformer

# Load the embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(prompt: str):
    """
    Convert a prompt into an embedding vector.
    """

    embedding = model.encode(
        prompt,
        convert_to_numpy=True
    )

    return embedding.tolist()
