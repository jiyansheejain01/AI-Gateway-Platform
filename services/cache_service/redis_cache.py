"""
Standard Redis cache operations for fast key-value lookups (metadata, sessions).
"""
import hashlib
import json

from .redis_client import r

# Cache responses for 5 minutes
CACHE_TTL = 5 * 60


def get_prompt_hash(prompt: str):
    """
    Generate a unique SHA-256 hash for the prompt.
    """

    # Remove extra spaces before hashing
    prompt = " ".join(prompt.strip().split())

    return hashlib.sha256(
        prompt.encode()
    ).hexdigest()


def get_cached_response(prompt: str):

    key = f"prompt:{get_prompt_hash(prompt)}"

    print("Looking for:", key)

    cached_response = r.get(key)

    print("Redis returned:", cached_response)

    if cached_response:
        return json.loads(cached_response)

    return None


def cache_response(prompt: str, response: dict):

    key = f"prompt:{get_prompt_hash(prompt)}"

    print("Saving Redis key:", key)

    r.set(
        key,
        json.dumps(response),
        ex=CACHE_TTL
    )

    print("Saved successfully")