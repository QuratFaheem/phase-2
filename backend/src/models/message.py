from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime
from enum import Enum

class Role(str, Enum):
    user = "user"
    assistant = "assistant"

class Message(SQLModel, table=True):
    __tablename__ = "messages"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(nullable=False)
    user_id: uuid.UUID = Field(nullable=False)
    role: Role = Field(nullable=False)
    content: str = Field(nullable=False, max_length=5000)
    created_at: datetime = Field(default_factory=datetime.utcnow)