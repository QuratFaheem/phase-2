from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from typing import Annotated, List
from ..database.connection import engine
from ..models.todo import Todo, TodoCreate, TodoUpdate, TodoRead
from ..services.todo_service import (
    create_todo, get_todos_by_user, get_todo_by_id_and_user,
    update_todo, delete_todo
)
from ..models.user import User
from jose import jwt, JWTError
from datetime import datetime
import uuid

router = APIRouter(prefix="/todos", tags=["todos"])

def get_session():
    with Session(engine) as session:
        yield session

# Simple token verification function (in a real app, you'd use FastAPI's security features)
def verify_token(authorization: str = Header(...)) -> dict:
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization[7:]  # Remove "Bearer " prefix

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"user_id": uuid.UUID(user_id)}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/", response_model=List[TodoRead])
def get_todos(session: Annotated[Session, Depends(get_session)],
              authorization: str = Header(...)):
    """Get all todos for the authenticated user."""
    user_info = verify_token(authorization)
    user_id = user_info["user_id"]

    todos = get_todos_by_user(user_id, session)
    return todos

@router.post("/", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_new_todo(todo_data: TodoCreate, session: Annotated[Session, Depends(get_session)],
                    authorization: str = Header(...)):
    """Create a new todo for the authenticated user."""
    user_info = verify_token(authorization)
    user_id = user_info["user_id"]

    todo = create_todo(todo_data, user_id, session)
    return todo

@router.get("/{todo_id}", response_model=TodoRead)
def get_todo(todo_id: uuid.UUID, session: Annotated[Session, Depends(get_session)],
             authorization: str = Header(...)):
    """Get a specific todo by ID for the authenticated user."""
    user_info = verify_token(authorization)
    user_id = user_info["user_id"]

    todo = get_todo_by_id_and_user(todo_id, user_id, session)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return todo

@router.put("/{todo_id}", response_model=TodoRead)
def update_existing_todo(
    todo_id: uuid.UUID,
    todo_update: TodoUpdate,
    session: Annotated[Session, Depends(get_session)],
    authorization: str = Header(...)
):
    """Update a specific todo for the authenticated user."""
    user_info = verify_token(authorization)
    user_id = user_info["user_id"]

    todo = update_todo(todo_id, todo_update, user_id, session)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_todo(todo_id: uuid.UUID, session: Annotated[Session, Depends(get_session)],
                         authorization: str = Header(...)):
    """Delete a specific todo for the authenticated user."""
    user_info = verify_token(authorization)
    user_id = user_info["user_id"]

    success = delete_todo(todo_id, user_id, session)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return