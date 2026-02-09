import pytest
from unittest.mock import AsyncMock, patch
from ai_agents.todo_agent import TodoAgent
from mcp_server.tools.list_tasks import ListTasksArgs
from mcp_server.tools.create_task import CreateTaskArgs
from mcp_server.tools.get_task import GetTaskArgs
from mcp_server.tools.update_task import UpdateTaskArgs
from mcp_server.tools.delete_task import DeleteTaskArgs
from mcp_server.tools.toggle_task import ToggleTaskArgs
from models.task import Task
import uuid
from datetime import datetime


@pytest.mark.asyncio
async def test_todo_agent_processes_create_task_request():
    """Test that the agent correctly processes a request to create a task."""
    agent = TodoAgent()
    user_id = str(uuid.uuid4())
    message = "Add a task to buy groceries"
    
    # Mock the OpenAI API response to call the create_task function
    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message = AsyncMock()
    mock_response.choices[0].message.tool_calls = [AsyncMock()]
    mock_response.choices[0].message.tool_calls[0].function = AsyncMock()
    mock_response.choices[0].message.tool_calls[0].function.name = "create_task"
    mock_response.choices[0].message.tool_calls[0].function.arguments = '{"user_id": "' + user_id + '", "title": "buy groceries", "description": ""}'
    mock_response.choices[0].message.tool_calls[0].id = "call_1"
    
    mock_final_response = AsyncMock()
    mock_final_response.choices = [AsyncMock()]
    mock_final_response.choices[0].message = AsyncMock()
    mock_final_response.choices[0].message.content = "I have added the task 'buy groceries' to your list."
    
    mock_task = Task(
        id=uuid.uuid4(),
        user_id=uuid.UUID(user_id),
        title="buy groceries",
        description="",
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    with patch.object(agent.client.chat.completions, 'create', side_effect=[mock_response, mock_final_response]), \
         patch('ai_agents.todo_agent.create_task_tool') as mock_create_task:
        
        mock_create_task.return_value = mock_task.dict()
        
        result = await agent.process_message(user_id, message)
        
        # Verify the create_task tool was called with correct arguments
        mock_create_task.assert_called_once()
        args_passed = mock_create_task.call_args[0][0]
        assert isinstance(args_passed, CreateTaskArgs)
        assert args_passed.user_id == user_id
        assert args_passed.title == "buy groceries"
        
        # Verify the response contains the expected content
        assert "buy groceries" in result["response"]
        assert len(result["tool_calls"]) == 1
        assert result["tool_calls"][0]["tool_name"] == "create_task"


@pytest.mark.asyncio
async def test_todo_agent_processes_list_tasks_request():
    """Test that the agent correctly processes a request to list tasks."""
    agent = TodoAgent()
    user_id = str(uuid.uuid4())
    message = "What are my tasks?"
    
    # Mock the OpenAI API response to call the list_tasks function
    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message = AsyncMock()
    mock_response.choices[0].message.tool_calls = [AsyncMock()]
    mock_response.choices[0].message.tool_calls[0].function = AsyncMock()
    mock_response.choices[0].message.tool_calls[0].function.name = "list_tasks"
    mock_response.choices[0].message.tool_calls[0].function.arguments = '{"user_id": "' + user_id + '"}'
    mock_response.choices[0].message.tool_calls[0].id = "call_1"
    
    mock_final_response = AsyncMock()
    mock_final_response.choices = [AsyncMock()]
    mock_final_response.choices[0].message = AsyncMock()
    mock_final_response.choices[0].message.content = "You have 1 task: buy groceries."
    
    mock_task = Task(
        id=uuid.uuid4(),
        user_id=uuid.UUID(user_id),
        title="buy groceries",
        description="",
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    with patch.object(agent.client.chat.completions, 'create', side_effect=[mock_response, mock_final_response]), \
         patch('ai_agents.todo_agent.list_tasks') as mock_list_tasks:
        
        mock_list_tasks.return_value = [mock_task.dict()]
        
        result = await agent.process_message(user_id, message)
        
        # Verify the list_tasks tool was called with correct arguments
        mock_list_tasks.assert_called_once()
        args_passed = mock_list_tasks.call_args[0][0]
        assert isinstance(args_passed, ListTasksArgs)
        assert args_passed.user_id == user_id
        
        # Verify the response contains the expected content
        assert "buy groceries" in result["response"]
        assert len(result["tool_calls"]) == 1
        assert result["tool_calls"][0]["tool_name"] == "list_tasks"


@pytest.mark.asyncio
async def test_todo_agent_handles_no_tool_calls():
    """Test that the agent handles requests that don't require tools."""
    agent = TodoAgent()
    user_id = str(uuid.uuid4())
    message = "Hello, how are you?"
    
    # Mock the OpenAI API response without tool calls
    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message = AsyncMock()
    mock_response.choices[0].message.tool_calls = None
    mock_response.choices[0].message.content = "I'm doing well, thank you for asking!"
    
    with patch.object(agent.client.chat.completions, 'create', return_value=mock_response):
        result = await agent.process_message(user_id, message)
        
        # Verify the response contains the expected content
        assert "doing well" in result["response"]
        assert len(result["tool_calls"]) == 0


@pytest.mark.asyncio
async def test_todo_agent_processes_update_task_request():
    """Test that the agent correctly processes a request to update a task."""
    agent = TodoAgent()
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())
    message = f"Update the task '{task_id}' to 'buy groceries and milk'"
    
    # Mock the OpenAI API response to call the update_task function
    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message = AsyncMock()
    mock_response.choices[0].message.tool_calls = [AsyncMock()]
    mock_response.choices[0].message.tool_calls[0].function = AsyncMock()
    mock_response.choices[0].message.tool_calls[0].function.name = "update_task"
    mock_response.choices[0].message.tool_calls[0].function.arguments = f'{{"user_id": "{user_id}", "task_id": "{task_id}", "title": "buy groceries and milk"}}'
    mock_response.choices[0].message.tool_calls[0].id = "call_1"
    
    mock_final_response = AsyncMock()
    mock_final_response.choices = [AsyncMock()]
    mock_final_response.choices[0].message = AsyncMock()
    mock_final_response.choices[0].message.content = "I have updated your task to 'buy groceries and milk'."
    
    mock_task = Task(
        id=uuid.UUID(task_id),
        user_id=uuid.UUID(user_id),
        title="buy groceries and milk",
        description="",
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    with patch.object(agent.client.chat.completions, 'create', side_effect=[mock_response, mock_final_response]), \
         patch('ai_agents.todo_agent.update_task_tool') as mock_update_task:
        
        mock_update_task.return_value = mock_task.dict()
        
        result = await agent.process_message(user_id, message)
        
        # Verify the update_task tool was called with correct arguments
        mock_update_task.assert_called_once()
        args_passed = mock_update_task.call_args[0][0]
        assert isinstance(args_passed, UpdateTaskArgs)
        assert args_passed.user_id == user_id
        assert args_passed.task_id == task_id
        assert args_passed.title == "buy groceries and milk"
        
        # Verify the response contains the expected content
        assert "buy groceries and milk" in result["response"]
        assert len(result["tool_calls"]) == 1
        assert result["tool_calls"][0]["tool_name"] == "update_task"


@pytest.mark.asyncio
async def test_todo_agent_handles_tool_execution_error():
    """Test that the agent handles errors during tool execution."""
    agent = TodoAgent()
    user_id = str(uuid.uuid4())
    message = "Add a task to buy groceries"
    
    # Mock the OpenAI API response to call the create_task function
    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message = AsyncMock()
    mock_response.choices[0].message.tool_calls = [AsyncMock()]
    mock_response.choices[0].message.tool_calls[0].function = AsyncMock()
    mock_response.choices[0].message.tool_calls[0].function.name = "create_task"
    mock_response.choices[0].message.tool_calls[0].function.arguments = '{"user_id": "' + user_id + '", "title": "buy groceries", "description": ""}'
    mock_response.choices[0].message.tool_calls[0].id = "call_1"
    
    mock_final_response = AsyncMock()
    mock_final_response.choices = [AsyncMock()]
    mock_final_response.choices[0].message = AsyncMock()
    mock_final_response.choices[0].message.content = "Sorry, I couldn't create that task due to an error."
    
    with patch.object(agent.client.chat.completions, 'create', side_effect=[mock_response, mock_final_response]), \
         patch('ai_agents.todo_agent.create_task_tool', side_effect=Exception("Database error")):
        
        result = await agent.process_message(user_id, message)
        
        # Verify the response indicates an error occurred
        assert "error" in result["response"].lower()
        assert len(result["tool_calls"]) == 1
        assert "error" in result["tool_calls"][0]["result"]