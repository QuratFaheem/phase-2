from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, sa_column_kwargs={"primary_key": True})
    email: str = Field(sa_column_kwargs={"nullable": False, "max_length": 255})
    name: Optional[str] = Field(default=None, sa_column_kwargs={"nullable": True, "max_length": 255})
    hashed_password: str = Field(sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)