from sqlmodel import Session, select
from database.connection import engine
from models.message import Message, Role
from models.conversation import Conversation
from typing import List
import uuid
from datetime import datetime


def create_message(
    conversation_id: str,
    user_id: str,
    role: Role,
    content: str
) -> Message:
    """Create a new message in a conversation."""
    with Session(engine) as session:
        message = Message(
            id=uuid.uuid4(),
            conversation_id=uuid.UUID(conversation_id),
            user_id=uuid.UUID(user_id),
            role=role,
            content=content,
            created_at=datetime.utcnow()
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message


def get_message_by_id(message_id: str, user_id: str) -> Message:
    """Get a specific message by its ID for a user."""
    with Session(engine) as session:
        statement = select(Message).where(
            Message.id == uuid.UUID(message_id),
            Message.user_id == uuid.UUID(user_id)
        )
        message = session.exec(statement).first()
        return message


def get_messages_by_conversation(
    conversation_id: str, 
    user_id: str, 
    limit: int = 50, 
    offset: int = 0
) -> List[Message]:
    """Get messages from a specific conversation for a user."""
    with Session(engine) as session:
        # First verify that the conversation belongs to the user
        conversation_statement = select(Conversation).where(
            Conversation.id == uuid.UUID(conversation_id),
            Conversation.user_id == uuid.UUID(user_id)
        )
        conversation = session.exec(conversation_statement).first()
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found for user {user_id}")
        
        statement = select(Message).where(
            Message.conversation_id == uuid.UUID(conversation_id)
        ).order_by(Message.created_at.asc()).offset(offset).limit(limit)
        messages = session.exec(statement).all()
        return messages


def update_message_content(message_id: str, user_id: str, new_content: str) -> Message:
    """Update the content of a message."""
    with Session(engine) as session:
        message = get_message_by_id(message_id, user_id)
        if not message:
            raise ValueError(f"Message {message_id} not found for user {user_id}")
        
        message.content = new_content
        message.created_at = datetime.utcnow()  # Update timestamp
        session.add(message)
        session.commit()
        session.refresh(message)
        return message


def delete_message(message_id: str, user_id: str) -> bool:
    """Delete a message."""
    with Session(engine) as session:
        message = get_message_by_id(message_id, user_id)
        if not message:
            return False
        
        session.delete(message)
        session.commit()
        return True


def count_messages_in_conversation(conversation_id: str, user_id: str) -> int:
    """Count the number of messages in a conversation for a user."""
    with Session(engine) as session:
        # First verify that the conversation belongs to the user
        conversation_statement = select(Conversation).where(
            Conversation.id == uuid.UUID(conversation_id),
            Conversation.user_id == uuid.UUID(user_id)
        )
        conversation = session.exec(conversation_statement).first()
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found for user {user_id}")
        
        statement = select(Message).where(
            Message.conversation_id == uuid.UUID(conversation_id)
        )
        count = session.exec(statement).count()
        return count