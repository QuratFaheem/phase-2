"""
MCP (Model Context Protocol) Server for Todo Application

This server exposes task operations as tools for the AI agent to use,
ensuring that AI agents never directly access the database.
"""
import asyncio
from typing import Dict, Any, List
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from middleware.jwt_auth import verify_token
from services.task_service import (
    create_task, get_tasks, get_task_by_id, 
    update_task, delete_task, toggle_task_completion
)

app = FastAPI(title="Todo MCP Server", version="1.0.0")

# Define the tool schemas
class ToolCall(BaseModel):
    id: str
    function: Dict[str, Any]

class ToolResult(BaseModel):
    tool_call_id: str
    result: Dict[str, Any]

class MCPRequest(BaseModel):
    tools: List[Dict[str, Any]]
    tool_calls: List[ToolCall]

class MCPResponse(BaseModel):
    tool_results: List[ToolResult]

@app.post("/mcp/call")
async def handle_tool_call(request: Dict[str, Any], token_data: dict = Depends(verify_token)):
    """
    Handle a tool call from the AI agent.
    The token_data contains the authenticated user info.
    """
    user_id = token_data.get("sub")
    
    # Get the tool name and arguments
    tool_name = request.get("tool_name")
    arguments = request.get("arguments", {})
    
    # Add the user_id to arguments for all operations
    arguments["user_id"] = user_id
    
    # Route to the appropriate tool function
    if tool_name == "list_tasks":
        result = await execute_list_tasks(arguments)
    elif tool_name == "create_task":
        result = await execute_create_task(arguments)
    elif tool_name == "get_task":
        result = await execute_get_task(arguments)
    elif tool_name == "update_task":
        result = await execute_update_task(arguments)
    elif tool_name == "delete_task":
        result = await execute_delete_task(arguments)
    elif tool_name == "toggle_task":
        result = await execute_toggle_task(arguments)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")
    
    return {"result": result}

async def execute_list_tasks(args: Dict[str, Any]):
    """Execute the list_tasks tool."""
    user_id = args.get("user_id")
    completed = args.get("completed")
    limit = args.get("limit", 50)
    offset = args.get("offset", 0)
    
    tasks = get_tasks(user_id=user_id, completed=completed, limit=limit, offset=offset)
    
    # Convert to dict for JSON serialization
    return [task.dict() for task in tasks]

async def execute_create_task(args: Dict[str, Any]):
    """Execute the create_task tool."""
    user_id = args.get("user_id")
    title = args.get("title")
    description = args.get("description")
    
    if not title:
        raise HTTPException(status_code=400, detail="Title is required for creating a task")
    
    task = create_task(user_id=user_id, title=title, description=description)
    return task.dict()

async def execute_get_task(args: Dict[str, Any]):
    """Execute the get_task tool."""
    user_id = args.get("user_id")
    task_id = args.get("task_id")
    
    if not task_id:
        raise HTTPException(status_code=400, detail="task_id is required for getting a task")
    
    task = get_task_by_id(task_id=task_id, user_id=user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task.dict()

async def execute_update_task(args: Dict[str, Any]):
    """Execute the update_task tool."""
    user_id = args.get("user_id")
    task_id = args.get("task_id")
    title = args.get("title")
    description = args.get("description")
    
    if not task_id:
        raise HTTPException(status_code=400, detail="task_id is required for updating a task")
    
    updated_task = update_task(task_id=task_id, user_id=user_id, title=title, description=description)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return updated_task.dict()

async def execute_delete_task(args: Dict[str, Any]):
    """Execute the delete_task tool."""
    user_id = args.get("user_id")
    task_id = args.get("task_id")
    
    if not task_id:
        raise HTTPException(status_code=400, detail="task_id is required for deleting a task")
    
    success = delete_task(task_id=task_id, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"success": True, "message": "Task deleted successfully"}

async def execute_toggle_task(args: Dict[str, Any]):
    """Execute the toggle_task tool."""
    user_id = args.get("user_id")
    task_id = args.get("task_id")
    completed = args.get("completed", False)
    
    if not task_id:
        raise HTTPException(status_code=400, detail="task_id is required for toggling task completion")
    
    task = toggle_task_completion(task_id=task_id, user_id=user_id, completed=completed)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task.dict()

@app.get("/")
async def root():
    return {"message": "Todo MCP Server is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)