from sqlmodel import Session, select
from database.connection import engine
from models.conversation import Conversation
from models.message import Message, Role
from typing import List
import uuid
from datetime import datetime


def create_conversation(user_id: str) -> Conversation:
    """Create a new conversation for a user."""
    with Session(engine) as session:
        conversation = Conversation(
            id=uuid.uuid4(),
            user_id=uuid.UUID(user_id),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation


def get_conversation_by_id(conversation_id: str, user_id: str) -> Conversation:
    """Get a specific conversation by its ID for a user."""
    with Session(engine) as session:
        statement = select(Conversation).where(
            Conversation.id == uuid.UUID(conversation_id),
            Conversation.user_id == uuid.UUID(user_id)
        )
        conversation = session.exec(statement).first()
        return conversation


def get_recent_conversations(user_id: str, limit: int = 10) -> List[Conversation]:
    """Get recent conversations for a user."""
    with Session(engine) as session:
        statement = select(Conversation).where(
            Conversation.user_id == uuid.UUID(user_id)
        ).order_by(Conversation.updated_at.desc()).limit(limit)
        conversations = session.exec(statement).all()
        return conversations


def add_message_to_conversation(
    conversation_id: str, 
    user_id: str, 
    role: Role, 
    content: str
) -> Message:
    """Add a message to a conversation."""
    with Session(engine) as session:
        # Verify the conversation belongs to the user
        conversation = get_conversation_by_id(conversation_id, user_id)
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found for user {user_id}")
        
        message = Message(
            id=uuid.uuid4(),
            conversation_id=uuid.UUID(conversation_id),
            user_id=uuid.UUID(user_id),
            role=role,
            content=content,
            created_at=datetime.utcnow()
        )
        session.add(message)
        # Update the conversation's updated_at timestamp
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()
        session.refresh(message)
        return message


def get_conversation_messages(conversation_id: str, user_id: str, limit: int = 50) -> List[Message]:
    """Get messages from a conversation."""
    with Session(engine) as session:
        # Verify the conversation belongs to the user
        conversation = get_conversation_by_id(conversation_id, user_id)
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found for user {user_id}")
        
        statement = select(Message).where(
            Message.conversation_id == uuid.UUID(conversation_id)
        ).order_by(Message.created_at.asc()).limit(limit)
        messages = session.exec(statement).all()
        return messages


def delete_conversation(conversation_id: str, user_id: str) -> bool:
    """Delete a conversation for a user."""
    with Session(engine) as session:
        conversation = get_conversation_by_id(conversation_id, user_id)
        if not conversation:
            return False
        
        session.delete(conversation)
        session.commit()
        return True