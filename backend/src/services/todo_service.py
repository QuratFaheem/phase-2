from sqlmodel import Session, select
from typing import Optional
from uuid import UUID
from ..models.todo import Todo, TodoCreate, TodoUpdate
from ..models.user import User

def create_todo(todo_data: TodoCreate, user_id: UUID, db_session: Session) -> Todo:
    """Create a new todo for a user."""
    todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        status=todo_data.status,
        user_id=user_id
    )

    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)

    return todo

def get_todos_by_user(user_id: UUID, db_session: Session) -> list[Todo]:
    """Get all todos for a specific user."""
    todos = db_session.exec(select(Todo).where(Todo.user_id == user_id)).all()
    return todos

def get_todo_by_id_and_user(todo_id: UUID, user_id: UUID, db_session: Session) -> Optional[Todo]:
    """Get a specific todo by ID for a specific user."""
    todo = db_session.exec(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    ).first()
    return todo

def update_todo(todo_id: UUID, todo_update: TodoUpdate, user_id: UUID, db_session: Session) -> Optional[Todo]:
    """Update a todo for a specific user."""
    todo = get_todo_by_id_and_user(todo_id, user_id, db_session)
    if not todo:
        return None

    # Update the todo with provided values
    update_data = todo_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)

    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)

    return todo

def delete_todo(todo_id: UUID, user_id: UUID, db_session: Session) -> bool:
    """Delete a todo for a specific user."""
    todo = get_todo_by_id_and_user(todo_id, user_id, db_session)
    if not todo:
        return False

    db_session.delete(todo)
    db_session.commit()

    return True