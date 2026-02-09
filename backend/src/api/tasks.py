from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlmodel import Session
from middleware.jwt_auth import get_current_user
from models.user import User
from models.task import Task, TaskBase
from services.task_service import (
    create_task, get_tasks, get_task_by_id, 
    update_task, delete_task, toggle_task_completion
)
from database.connection import engine
import uuid

router = APIRouter()

@router.get("/api/{user_id}/tasks", response_model=List[Task])
def read_tasks(
    user_id: str,
    completed: Optional[bool] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user)
):
    # Verify that the user_id in the path matches the authenticated user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access these tasks")
    
    tasks = get_tasks(user_id=user_id, completed=completed, limit=limit, offset=offset)
    return tasks


@router.post("/api/{user_id}/tasks", response_model=Task)
def create_new_task(
    user_id: str,
    task: TaskBase,
    current_user: User = Depends(get_current_user)
):
    # Verify that the user_id in the path matches the authenticated user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to create tasks for this user")
    
    created_task = create_task(
        user_id=user_id,
        title=task.title,
        description=task.description
    )
    return created_task


@router.get("/api/{user_id}/tasks/{task_id}", response_model=Task)
def read_task(
    user_id: str,
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    # Verify that the user_id in the path matches the authenticated user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access these tasks")
    
    task = get_task_by_id(task_id=task_id, user_id=user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/api/{user_id}/tasks/{task_id}", response_model=Task)
def update_existing_task(
    user_id: str,
    task_id: str,
    task: TaskBase,
    current_user: User = Depends(get_current_user)
):
    # Verify that the user_id in the path matches the authenticated user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update tasks for this user")
    
    updated_task = update_task(
        task_id=task_id,
        user_id=user_id,
        title=task.title,
        description=task.description
    )
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/api/{user_id}/tasks/{task_id}")
def delete_existing_task(
    user_id: str,
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    # Verify that the user_id in the path matches the authenticated user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete tasks for this user")
    
    success = delete_task(task_id=task_id, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@router.patch("/api/{user_id}/tasks/{task_id}/complete")
def toggle_task_complete(
    user_id: str,
    task_id: str,
    completed: bool,
    current_user: User = Depends(get_current_user)
):
    # Verify that the user_id in the path matches the authenticated user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update tasks for this user")
    
    task = toggle_task_completion(task_id=task_id, user_id=user_id, completed=completed)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task