"""
MCP Tool: list_tasks

Retrieve all tasks for the authenticated user.
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from services.task_service import get_tasks


class ListTasksArgs(BaseModel):
    user_id: str
    completed: Optional[bool] = None
    limit: int = 50
    offset: int = 0


async def list_tasks(args: ListTasksArgs) -> List[Dict[str, Any]]:
    """
    Retrieve all tasks for the specified user with optional filtering.
    
    Args:
        user_id: The ID of the user whose tasks to retrieve
        completed: Optional filter for completion status (true/false)
        limit: Number of tasks to return (default: 50, max: 100)
        offset: Number of tasks to skip (for pagination)
        
    Returns:
        List of task objects
    """
    # Validate arguments
    if args.limit > 100:
        args.limit = 100  # Cap the limit at 100
    
    # Call the service function
    tasks = get_tasks(
        user_id=args.user_id,
        completed=args.completed,
        limit=args.limit,
        offset=args.offset
    )
    
    # Convert tasks to dictionaries for JSON serialization
    return [task.dict() for task in tasks]