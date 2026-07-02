"""
Conversation memory using Redis.
Stores chat history for each session.
"""

import json

from services.cache_service.redis_client import r


SESSION_PREFIX = "chat_session:"

# Maximum number of messages to keep
MAX_HISTORY = 20


def load_conversation(session_id: str):

    key = SESSION_PREFIX + session_id

    print("Loading key:", key)

    history = r.get(key)

    print("Redis returned:", history)

    if history is None:
        return []

    return json.loads(history)


def save_conversation(session_id: str, history: list):

    history = history[-MAX_HISTORY:]

    key = SESSION_PREFIX + session_id

    print("\n===== SAVING TO REDIS =====")
    print("Key:", key)
    print("History:", history)

    r.set(
        key,
        json.dumps(history)
    )

    print("Redis value after save:", r.get(key))
    print("===========================\n")


def clear_conversation(session_id: str):

    key = SESSION_PREFIX + session_id

    r.delete(key)