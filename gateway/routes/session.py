"""
Conversation session routes.
"""

from fastapi import APIRouter

from services.memory_service.conversation_memory import clear_conversation

router = APIRouter(
    tags=["Sessions"],
)


@router.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    """
    Clear a conversation session.
    """

    clear_conversation(session_id)

    return {
        "message": f"Conversation '{session_id}' cleared successfully."
    }