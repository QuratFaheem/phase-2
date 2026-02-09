from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from middleware.jwt_auth import get_current_user
from models.user import User
from services.conversation_service import (
    create_conversation, get_conversation_by_id,
    add_message_to_conversation, get_conversation_messages
)
from services.message_service import get_messages_by_conversation
from ai_agents.todo_agent import TodoAgent
from models.message import Role
import uuid

router = APIRouter()
agent = TodoAgent()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

@router.post("/api/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    # Verify that the user_id in the path matches the authenticated user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this chat")

    message = request.message
    conversation_id = request.conversation_id

    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    # If no conversation ID is provided, create a new conversation
    if not conversation_id:
        conversation = create_conversation(user_id)
        conversation_id = str(conversation.id)
    else:
        # Validate that the conversation belongs to the user
        conv = get_conversation_by_id(conversation_id, user_id)
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found or does not belong to user")

    # Add the user's message to the conversation
    user_message = add_message_to_conversation(
        conversation_id=conversation_id,
        user_id=user_id,
        role=Role.user,
        content=message
    )

    # Process the message with the AI agent
    try:
        result = await agent.process_message(user_id, message)

        # Add the AI's response to the conversation
        ai_message = add_message_to_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
            role=Role.assistant,
            content=result["response"]
        )

        return {
            "success": True,
            "data": {
                "conversation_id": conversation_id,
                "response": result["response"],
                "tool_calls": result["tool_calls"],
                "timestamp": result["timestamp"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@router.get("/api/{user_id}/conversations/{conversation_id}/messages")
async def get_chat_history(
    user_id: str,
    conversation_id: str,
    limit: int = 50,
    current_user: User = Depends(get_current_user)
):
    # Verify that the user_id in the path matches the authenticated user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this chat history")
    
    try:
        messages = get_messages_by_conversation(conversation_id, user_id, limit)
        return {
            "success": True,
            "data": {
                "messages": [msg.dict() for msg in messages]
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))