"""
Chat routes.
"""

from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel

from core.security import get_current_user
from services.chat_service.service import process_chat

router = APIRouter()


class PromptRequest(BaseModel):
    session_id: str
    prompt: str


@router.post("/chat")
def chat(
    request: PromptRequest,
    current_user=Depends(get_current_user),
):
    """
    Protected chat endpoint.
    """

    return process_chat(
        session_id=request.session_id,
        prompt=request.prompt,
        current_user=current_user,
    )