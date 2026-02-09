from sqlmodel import Session, select
from database.connection import engine
from models.task import Task, TaskBase
from models.user import User
from typing import List, Optional
import uuid
from datetime import datetime


def create_task(user_id: str, title: str, description: Optional[str] = None) -> Task:
    """Create a new task for a user."""
    with Session(engine) as session:
        task = Task(
            id=uuid.uuid4(),
            user_id=uuid.UUID(user_id),
            title=title,
            description=description,
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task


def get_tasks(user_id: str, completed: Optional[bool] = None, limit: int = 50, offset: int = 0) -> List[Task]:
    """Get all tasks for a user with optional filtering."""
    with Session(engine) as session:
        statement = select(Task).where(Task.user_id == uuid.UUID(user_id))
        
        if completed is not None:
            statement = statement.where(Task.completed == completed)
            
        statement = statement.offset(offset).limit(limit)
        tasks = session.exec(statement).all()
        return tasks


def get_task_by_id(task_id: str, user_id: str) -> Optional[Task]:
    """Get a specific task by its ID for a user."""
    with Session(engine) as session:
        statement = select(Task).where(
            Task.id == uuid.UUID(task_id),
            Task.user_id == uuid.UUID(user_id)
        )
        task = session.exec(statement).first()
        return task


def update_task(task_id: str, user_id: str, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
    """Update a task for a user."""
    with Session(engine) as session:
        task = get_task_by_id(task_id, user_id)
        if not task:
            return None
            
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        task.updated_at = datetime.utcnow()
        
        session.add(task)
        session.commit()
        session.refresh(task)
        return task


def delete_task(task_id: str, user_id: str) -> bool:
    """Delete a task for a user."""
    with Session(engine) as session:
        task = get_task_by_id(task_id, user_id)
        if not task:
            return False
            
        session.delete(task)
        session.commit()
        return True


def toggle_task_completion(task_id: str, user_id: str, completed: bool) -> Optional[Task]:
    """Toggle the completion status of a task for a user."""
    with Session(engine) as session:
        task = get_task_by_id(task_id, user_id)
        if not task:
            return None
            
        task.completed = completed
        task.updated_at = datetime.utcnow()
        
        session.add(task)
        session.commit()
        session.refresh(task)
        return task