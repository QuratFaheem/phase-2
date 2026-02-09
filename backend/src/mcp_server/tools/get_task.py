"""
MCP Tool: get_task

Retrieve a specific task for the authenticated user.
"""
from typing import Dict, Any
from pydantic import BaseModel
from services.task_service import get_task_by_id


class GetTaskArgs(BaseModel):
    user_id: str
    task_id: str


async def get_task(args: GetTaskArgs) -> Dict[str, Any]:
    """
    Retrieve a specific task for the specified user.
    
    Args:
        user_id: The ID of the user (must match JWT user ID)
        task_id: The ID of the task to retrieve
        
    Returns:
        The requested task object
        
    Raises:
        ValueError: If the task is not found
    """
    # Validate arguments
    if not args.task_id:
        raise ValueError("task_id is required")
    
    if not args.user_id:
        raise ValueError("user_id is required")
    
    # Call the service function
    task = get_task_by_id(task_id=args.task_id, user_id=args.user_id)
    
    if not task:
        raise ValueError(f"Task with ID {args.task_id} not found for user {args.user_id}")
    
    # Convert task to dictionary for JSON serialization
    return task.dict()