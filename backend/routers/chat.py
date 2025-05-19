from fastapi import APIRouter
from backend.schemas.chat_schema import ChatRequest, ChatResponse
from backend.services.chat_service import process_message

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/")
async def chat(req: ChatRequest) -> ChatResponse:
    reply = process_message(req.message)
    return ChatResponse(reply=reply)