"""
Conversation memory using Redis.
Stores chat history for each user session.
"""

import json

from core.logging import logger
from services.cache_service.redis_client import r


SESSION_PREFIX = "chat_session"

# Maximum number of messages to keep
MAX_HISTORY = 20


def build_session_key(
    tenant: str,
    user_id: str,
    session_id: str,
) -> str:
    """
    Build a unique Redis key for a user's conversation.
    """

    return f"{SESSION_PREFIX}:{tenant}:{user_id}:{session_id}"


def load_conversation(
    tenant: str,
    user_id: str,
    session_id: str,
):
    """
    Load a conversation from Redis.
    """

    key = build_session_key(
        tenant,
        user_id,
        session_id,
    )

    logger.info(
        "Loading conversation",
        key=key,
    )

    history = r.get(key)

    if history is None:
        return []

    return json.loads(history)


def save_conversation(
    tenant: str,
    user_id: str,
    session_id: str,
    history: list,
):
    """
    Save conversation history.
    """

    history = history[-MAX_HISTORY:]

    key = build_session_key(
        tenant,
        user_id,
        session_id,
    )

    r.set(
        key,
        json.dumps(history),
    )

    logger.info(
        "Conversation saved",
        key=key,
        messages=len(history),
    )


def clear_conversation(
    tenant: str,
    user_id: str,
    session_id: str,
):
    """
    Delete a conversation.
    """

    key = build_session_key(
        tenant,
        user_id,
        session_id,
    )

    r.delete(key)