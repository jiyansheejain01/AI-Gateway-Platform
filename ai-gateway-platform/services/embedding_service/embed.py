"""
Service to generate embeddings using OpenAI, HuggingFace, or Cohere models.
"""
"""
from sentence_transformers import SentenceTransformer

# Load the embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(prompt: str):
    

    embedding = model.encode(
        prompt,
        convert_to_numpy=True
    )

    return embedding.tolist()
"""

"""
TEMP DEBUG VERSION
"""

def generate_embedding(prompt: str):
    # Return a dummy embedding
    return [0.0] * 384