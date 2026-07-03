"""
Conversation session routes.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from services.memory_service.conversation_memory import clear_conversation

router = APIRouter()


class SessionRequest(BaseModel):
    session_id: str


@router.delete("/new_chat")
def new_chat(request: SessionRequest):

    clear_conversation(request.session_id)

    return {
        "message": f"Conversation '{request.session_id}' cleared successfully."
    }