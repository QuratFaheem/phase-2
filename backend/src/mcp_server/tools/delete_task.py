"""
MCP Tool: delete_task

Delete a specific task for the authenticated user.
"""
from typing import Dict, Any
from pydantic import BaseModel
from services.task_service import delete_task


class DeleteTaskArgs(BaseModel):
    user_id: str
    task_id: str


async def delete_task_tool(args: DeleteTaskArgs) -> Dict[str, Any]:
    """
    Delete a specific task for the specified user.
    
    Args:
        user_id: The ID of the user (must match JWT user ID)
        task_id: The ID of the task to delete
        
    Returns:
        Success message if the task was deleted
        
    Raises:
        ValueError: If the task is not found
    """
    # Validate arguments
    if not args.task_id:
        raise ValueError("task_id is required")
    
    if not args.user_id:
        raise ValueError("user_id is required")
    
    # Call the service function
    success = delete_task(task_id=args.task_id, user_id=args.user_id)
    
    if not success:
        raise ValueError(f"Task with ID {args.task_id} not found for user {args.user_id}")
    
    # Return success message
    return {"success": True, "message": "Task deleted successfully"}