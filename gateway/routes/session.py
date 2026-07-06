"""
Conversation session routes.
"""

from fastapi import APIRouter
from fastapi import Depends

from core.security import get_current_user
from services.memory_service.conversation_memory import clear_conversation

router = APIRouter(
    tags=["Sessions"],
)


@router.delete("/sessions/{session_id}")
def delete_session(
    session_id: str,
    current_user=Depends(get_current_user),
):
    """
    Delete a conversation session.
    """

    user_id = current_user["sub"]
    tenant = current_user["tenant"]

    clear_conversation(
        tenant=tenant,
        user_id=user_id,
        session_id=session_id,
    )

    return {
        "message": f"Conversation '{session_id}' deleted successfully."
    }