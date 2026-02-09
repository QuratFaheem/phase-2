from sqlmodel import SQLModel
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from typing import Optional

# Test with a minimal model using SQLAlchemy column definitions (compatible with older SQLModel)
class TestUser(SQLModel, table=True):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, default="test@example.com")
    name = Column(String, default=None)
    hashed_password = Column(String, default="default_hash")

print("TestUser model defined successfully")