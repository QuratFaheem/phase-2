from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime
from typing import Optional

# Test with a minimal model using the latest SQLModel syntax
class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    hashed_password: str = Field(nullable=False)

print("User model defined successfully")