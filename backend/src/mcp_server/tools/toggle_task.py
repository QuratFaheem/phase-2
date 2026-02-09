"""
MCP Tool: toggle_task

Toggle the completion status of a specific task for the authenticated user.
"""
from typing import Dict, Any
from pydantic import BaseModel
from services.task_service import toggle_task_completion


class ToggleTaskArgs(BaseModel):
    user_id: str
    task_id: str
    completed: bool


async def toggle_task(args: ToggleTaskArgs) -> Dict[str, Any]:
    """
    Toggle the completion status of a specific task for the specified user.
    
    Args:
        user_id: The ID of the user (must match JWT user ID)
        task_id: The ID of the task to update
        completed: The new completion status for the task
        
    Returns:
        The updated task object
        
    Raises:
        ValueError: If the task is not found
    """
    # Validate arguments
    if not args.task_id:
        raise ValueError("task_id is required")
    
    if not args.user_id:
        raise ValueError("user_id is required")
    
    # Call the service function
    task = toggle_task_completion(
        task_id=args.task_id,
        user_id=args.user_id,
        completed=args.completed
    )
    
    if not task:
        raise ValueError(f"Task with ID {args.task_id} not found for user {args.user_id}")
    
    # Convert task to dictionary for JSON serialization
    return task.dict()