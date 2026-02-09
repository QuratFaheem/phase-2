"""
MCP Tool: update_task

Update a specific task for the authenticated user.
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel
from services.task_service import update_task


class UpdateTaskArgs(BaseModel):
    user_id: str
    task_id: str
    title: Optional[str] = None
    description: Optional[str] = None


async def update_task_tool(args: UpdateTaskArgs) -> Dict[str, Any]:
    """
    Update a specific task for the specified user.
    
    Args:
        user_id: The ID of the user (must match JWT user ID)
        task_id: The ID of the task to update
        title: Optional new title for the task
        description: Optional new description for the task
        
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
    
    if args.title and len(args.title) > 200:
        raise ValueError("Title must be 200 characters or less")
    
    if args.description and len(args.description) > 1000:
        raise ValueError("Description must be 1000 characters or less")
    
    # Call the service function
    updated_task = update_task(
        task_id=args.task_id,
        user_id=args.user_id,
        title=args.title,
        description=args.description
    )
    
    if not updated_task:
        raise ValueError(f"Task with ID {args.task_id} not found for user {args.user_id}")
    
    # Convert task to dictionary for JSON serialization
    return updated_task.dict()