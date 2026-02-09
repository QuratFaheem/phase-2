"""
MCP Tool: create_task

Create a new task for the authenticated user.
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel
from services.task_service import create_task


class CreateTaskArgs(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = None


async def create_task_tool(args: CreateTaskArgs) -> Dict[str, Any]:
    """
    Create a new task for the specified user.
    
    Args:
        user_id: The ID of the user creating the task
        title: The title of the task
        description: Optional description of the task
        
    Returns:
        The created task object
    """
    # Validate arguments
    if not args.title or len(args.title.strip()) == 0:
        raise ValueError("Title is required and cannot be empty")
    
    if len(args.title) > 200:
        raise ValueError("Title must be 200 characters or less")
    
    if args.description and len(args.description) > 1000:
        raise ValueError("Description must be 1000 characters or less")
    
    # Call the service function
    task = create_task(
        user_id=args.user_id,
        title=args.title,
        description=args.description
    )
    
    # Convert task to dictionary for JSON serialization
    return task.dict()