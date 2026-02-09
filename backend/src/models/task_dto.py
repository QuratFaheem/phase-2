from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class TaskResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime