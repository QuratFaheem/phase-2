from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid
from pydantic import field_validator

class UserBase(SQLModel):
    name: str = Field(max_length=100)
    email: str = Field(unique=True, max_length=255)

class User(UserBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    password_hash: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    password: str

    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v):
        if len(v) > 72:
            raise ValueError('Password must not exceed 72 characters')
        return v

class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime

class UserLogin(SQLModel):
    email: str
    password: str

    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v):
        if len(v) > 72:
            raise ValueError('Password must not exceed 72 characters')
        return v