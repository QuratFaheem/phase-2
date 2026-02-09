import pytest
from unittest.mock import AsyncMock, patch
from mcp_server.tools.list_tasks import list_tasks, ListTasksArgs
from mcp_server.tools.create_task import create_task_tool, CreateTaskArgs
from mcp_server.tools.get_task import get_task, GetTaskArgs
from mcp_server.tools.update_task import update_task_tool, UpdateTaskArgs
from mcp_server.tools.delete_task import delete_task_tool, DeleteTaskArgs
from mcp_server.tools.toggle_task import toggle_task, ToggleTaskArgs
from models.task import Task
import uuid
from datetime import datetime


@pytest.mark.asyncio
async def test_list_tasks():
    """Test the list_tasks tool."""
    args = ListTasksArgs(user_id=str(uuid.uuid4()), completed=None, limit=10, offset=0)
    
    mock_task = Task(
        id=uuid.uuid4(),
        user_id=uuid.UUID(args.user_id),
        title="Test Task",
        description="Test Description",
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    with patch('mcp_server.tools.list_tasks.get_tasks', return_value=[mock_task]) as mock_get_tasks:
        result = await list_tasks(args)
        
        # Verify the function was called with correct arguments
        mock_get_tasks.assert_called_once_with(
            user_id=args.user_id,
            completed=args.completed,
            limit=args.limit,
            offset=args.offset
        )
        
        # Verify the result
        assert len(result) == 1
        assert result[0]['title'] == "Test Task"


@pytest.mark.asyncio
async def test_create_task():
    """Test the create_task tool."""
    user_id = str(uuid.uuid4())
    args = CreateTaskArgs(user_id=user_id, title="New Task", description="New Description")
    
    mock_task = Task(
        id=uuid.uuid4(),
        user_id=uuid.UUID(user_id),
        title=args.title,
        description=args.description,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    with patch('mcp_server.tools.create_task.create_task', return_value=mock_task) as mock_create_task:
        result = await create_task_tool(args)
        
        # Verify the function was called with correct arguments
        mock_create_task.assert_called_once_with(
            user_id=args.user_id,
            title=args.title,
            description=args.description
        )
        
        # Verify the result
        assert result['title'] == args.title
        assert result['description'] == args.description


@pytest.mark.asyncio
async def test_get_task():
    """Test the get_task tool."""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())
    args = GetTaskArgs(user_id=user_id, task_id=task_id)
    
    mock_task = Task(
        id=uuid.UUID(task_id),
        user_id=uuid.UUID(user_id),
        title="Existing Task",
        description="Existing Description",
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    with patch('mcp_server.tools.get_task.get_task_by_id', return_value=mock_task) as mock_get_task_by_id:
        result = await get_task(args)
        
        # Verify the function was called with correct arguments
        mock_get_task_by_id.assert_called_once_with(task_id=task_id, user_id=user_id)
        
        # Verify the result
        assert result['title'] == "Existing Task"


@pytest.mark.asyncio
async def test_get_task_not_found():
    """Test the get_task tool when task is not found."""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())
    args = GetTaskArgs(user_id=user_id, task_id=task_id)
    
    with patch('mcp_server.tools.get_task.get_task_by_id', return_value=None):
        with pytest.raises(ValueError, match=f"Task with ID {task_id} not found for user {user_id}"):
            await get_task(args)


@pytest.mark.asyncio
async def test_update_task():
    """Test the update_task tool."""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())
    args = UpdateTaskArgs(user_id=user_id, task_id=task_id, title="Updated Task", description="Updated Description")
    
    mock_task = Task(
        id=uuid.UUID(task_id),
        user_id=uuid.UUID(user_id),
        title=args.title,
        description=args.description,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    with patch('mcp_server.tools.update_task.update_task', return_value=mock_task) as mock_update_task:
        result = await update_task_tool(args)
        
        # Verify the function was called with correct arguments
        mock_update_task.assert_called_once_with(
            task_id=task_id,
            user_id=user_id,
            title=args.title,
            description=args.description
        )
        
        # Verify the result
        assert result['title'] == args.title
        assert result['description'] == args.description


@pytest.mark.asyncio
async def test_update_task_not_found():
    """Test the update_task tool when task is not found."""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())
    args = UpdateTaskArgs(user_id=user_id, task_id=task_id, title="Updated Task")
    
    with patch('mcp_server.tools.update_task.update_task', return_value=None):
        with pytest.raises(ValueError, match=f"Task with ID {task_id} not found for user {user_id}"):
            await update_task_tool(args)


@pytest.mark.asyncio
async def test_delete_task():
    """Test the delete_task tool."""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())
    args = DeleteTaskArgs(user_id=user_id, task_id=task_id)
    
    with patch('mcp_server.tools.delete_task.delete_task', return_value=True) as mock_delete_task:
        result = await delete_task_tool(args)
        
        # Verify the function was called with correct arguments
        mock_delete_task.assert_called_once_with(task_id=task_id, user_id=user_id)
        
        # Verify the result
        assert result['success'] is True
        assert result['message'] == "Task deleted successfully"


@pytest.mark.asyncio
async def test_delete_task_not_found():
    """Test the delete_task tool when task is not found."""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())
    args = DeleteTaskArgs(user_id=user_id, task_id=task_id)
    
    with patch('mcp_server.tools.delete_task.delete_task', return_value=False):
        with pytest.raises(ValueError, match=f"Task with ID {task_id} not found for user {user_id}"):
            await delete_task_tool(args)


@pytest.mark.asyncio
async def test_toggle_task():
    """Test the toggle_task tool."""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())
    args = ToggleTaskArgs(user_id=user_id, task_id=task_id, completed=True)
    
    mock_task = Task(
        id=uuid.UUID(task_id),
        user_id=uuid.UUID(user_id),
        title="Test Task",
        description="Test Description",
        completed=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    with patch('mcp_server.tools.toggle_task.toggle_task_completion', return_value=mock_task) as mock_toggle_task_completion:
        result = await toggle_task(args)
        
        # Verify the function was called with correct arguments
        mock_toggle_task_completion.assert_called_once_with(
            task_id=task_id,
            user_id=user_id,
            completed=True
        )
        
        # Verify the result
        assert result['completed'] is True


@pytest.mark.asyncio
async def test_toggle_task_not_found():
    """Test the toggle_task tool when task is not found."""
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())
    args = ToggleTaskArgs(user_id=user_id, task_id=task_id, completed=True)
    
    with patch('mcp_server.tools.toggle_task.toggle_task_completion', return_value=None):
        with pytest.raises(ValueError, match=f"Task with ID {task_id} not found for user {user_id}"):
            await toggle_task(args)


@pytest.mark.asyncio
async def test_create_task_validation():
    """Test validation in create_task tool."""
    user_id = str(uuid.uuid4())
    
    # Test with empty title
    args = CreateTaskArgs(user_id=user_id, title="", description="Description")
    
    with pytest.raises(ValueError, match="Title is required and cannot be empty"):
        await create_task_tool(args)
    
    # Test with title too long
    long_title = "a" * 201
    args = CreateTaskArgs(user_id=user_id, title=long_title, description="Description")
    
    with pytest.raises(ValueError, match="Title must be 200 characters or less"):
        await create_task_tool(args)
    
    # Test with description too long
    long_desc = "a" * 1001
    args = CreateTaskArgs(user_id=user_id, title="Valid Title", description=long_desc)
    
    with pytest.raises(ValueError, match="Description must be 1000 characters or less"):
        await create_task_tool(args)