from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)