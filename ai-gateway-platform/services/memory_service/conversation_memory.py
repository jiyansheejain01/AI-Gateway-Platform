"""
Conversation memory using Redis.
Stores chat history for each user session.
"""

import json
from datetime import datetime
from core.logging import logger
from services.cache_service.redis_client import r


SESSION_PREFIX = "chat_session"
META_PREFIX = "conversation_meta"

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


def build_meta_key(
    tenant: str,
    user_id: str,
) -> str:
    """
    Redis key storing conversation list.
    """

    return f"{META_PREFIX}:{tenant}:{user_id}"


def update_conversation_metadata(
    tenant: str,
    user_id: str,
    session_id: str,
    history: list,
):
    """
    Maintain conversation list for sidebar.
    """

    key = build_meta_key(
        tenant,
        user_id,
    )

    metadata = r.get(key)

    if metadata:
        metadata = json.loads(metadata)
    else:
        metadata = []

    title = "New Conversation"

    for message in history:
        if message["role"] == "user":
            title = message["content"][:50]
            break

    updated = False

    for item in metadata:

        if item["session_id"] == session_id:

            item["title"] = title
            item["updated_at"] = datetime.utcnow().isoformat()

            updated = True
            break

    if not updated:

        metadata.append(
            {
                "session_id": session_id,
                "title": title,
                "updated_at": datetime.utcnow().isoformat(),
            }
        )

    metadata.sort(
        key=lambda x: x["updated_at"],
        reverse=True,
    )

    print("=" * 60)
    print("UPDATING METADATA")
    print("Key:", key)
    print("Metadata:", metadata)
    print("=" * 60)
    r.set(
        key,
        json.dumps(metadata),
    )


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

    print("=" * 60)
    print("SAVE CONVERSATION")
    print("Tenant:", tenant)
    print("User ID:", user_id)
    print("Session ID:", session_id)
    print("Session Key:", key)
    print("Meta Key:", build_meta_key(tenant, user_id))
    print("Messages:", history)
    print("=" * 60)
    r.set(
    key,
    json.dumps(history),
    )

    # Update conversation list
    update_conversation_metadata(
        tenant,
        user_id,
        session_id,
        history,
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