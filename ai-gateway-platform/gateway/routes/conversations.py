"""
Conversation routes.
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
import json

from core.security import get_current_user
from services.memory_service.conversation_memory import (
    build_meta_key,
    load_conversation,
    clear_conversation,
)
from services.cache_service.redis_client import r

router = APIRouter(
    tags=["Conversations"],
)


@router.get("/conversations")
def get_conversations(
    current_user=Depends(get_current_user),
):
    """
    Return all conversations for the logged-in user.
    """

    tenant = current_user["tenant"]
    user_id = current_user["sub"]

    key = build_meta_key(
        tenant,
        user_id,
    )

    metadata = r.get(key)

    if metadata is None:
        return []

    return json.loads(metadata)


@router.get("/conversation/{session_id}")
def get_conversation(
    session_id: str,
    current_user=Depends(get_current_user),
):
    """
    Return conversation history.
    """

    tenant = current_user["tenant"]
    user_id = current_user["sub"]

    history = load_conversation(
        tenant=tenant,
        user_id=user_id,
        session_id=session_id,
    )

    return history


@router.delete("/conversation/{session_id}")
def delete_conversation(
    session_id: str,
    current_user=Depends(get_current_user),
):
    """
    Delete a conversation.
    """

    tenant = current_user["tenant"]
    user_id = current_user["sub"]

    clear_conversation(
        tenant=tenant,
        user_id=user_id,
        session_id=session_id,
    )

    # ---------------- Remove sidebar metadata ---------------- #

    key = build_meta_key(
        tenant,
        user_id,
    )

    metadata = r.get(key)

    if metadata:

        metadata = json.loads(metadata)

        metadata = [
            item
            for item in metadata
            if item["session_id"] != session_id
        ]

        r.set(
            key,
            json.dumps(metadata),
        )

    return {
        "message": "Conversation deleted successfully."
    }