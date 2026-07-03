from fastapi import APIRouter
from pydantic import BaseModel

from services.chat_service.service import process_chat

router = APIRouter()


class PromptRequest(BaseModel):
    session_id: str
    prompt: str


@router.post("/chat")
def chat(request: PromptRequest):

    return process_chat(
        session_id=request.session_id,
        prompt=request.prompt,
    )