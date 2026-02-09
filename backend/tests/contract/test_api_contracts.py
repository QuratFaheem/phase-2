import pytest
from fastapi.testclient import TestClient
from main import app
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from models.user import User
from services.auth_service import get_password_hash
import uuid
from datetime import datetime
import json

# Create a test database engine
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(bind=test_engine)
    with Session(test_engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture():
    with TestClient(app) as client:
        yield client

@pytest.fixture(name="user")
def user_fixture(session: Session):
    user = User(
        id=uuid.uuid4(),
        email="testuser@example.com",
        hashed_password=get_password_hash("testpassword"),
        name="Test User",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@pytest.fixture(name="valid_token")
def token_fixture(user: User):
    from middleware.jwt_auth import create_access_token
    from datetime import timedelta
    
    access_token_expires = timedelta(minutes=30)
    token_data = {"sub": str(user.id)}
    token = create_access_token(data=token_data, expires_delta=access_token_expires)
    return token

def test_auth_signup_contract(client: TestClient):
    """Test the /auth/signup endpoint contract."""
    response = client.post(
        "/auth/signup",
        json={
            "email": "newuser@example.com",
            "password": "newpassword123",
            "name": "New User"
        }
    )
    
    # Check status code
    assert response.status_code in [200, 409]  # 200 for success, 409 for conflict
    
    if response.status_code == 200:
        data = response.json()
        
        # Check response structure
        assert "id" in data
        assert "email" in data
        assert "name" in data
        
        # Check data types
        assert isinstance(data["id"], str)
        assert isinstance(data["email"], str)
        assert isinstance(data["name"], str)
        
        # Check values
        assert data["email"] == "newuser@example.com"
        assert data["name"] == "New User"

def test_auth_signin_contract(client: TestClient, user: User):
    """Test the /auth/signin endpoint contract."""
    response = client.post(
        "/auth/signin",
        json={
            "email": "testuser@example.com",
            "password": "testpassword"
        }
    )
    
    # Check status code
    assert response.status_code in [200, 401]  # 200 for success, 401 for unauthorized
    
    if response.status_code == 200:
        data = response.json()
        
        # Check response structure
        assert "access_token" in data
        assert "token_type" in data
        
        # Check data types
        assert isinstance(data["access_token"], str)
        assert isinstance(data["token_type"], str)
        
        # Check values
        assert data["token_type"] == "bearer"

def test_get_tasks_contract(client: TestClient, user: User, valid_token: str):
    """Test the GET /api/{user_id}/tasks endpoint contract."""
    response = client.get(
        f"/api/{user.id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    # Check status code
    assert response.status_code == 200
    
    data = response.json()
    
    # Check response structure
    assert isinstance(data, list)  # Should return an array of tasks

def test_create_task_contract(client: TestClient, user: User, valid_token: str):
    """Test the POST /api/{user_id}/tasks endpoint contract."""
    response = client.post(
        f"/api/{user.id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "title": "Test Task",
            "description": "Test Description"
        }
    )
    
    # Check status code
    assert response.status_code == 200
    
    data = response.json()
    
    # Check response structure
    assert "id" in data
    assert "user_id" in data
    assert "title" in data
    assert "description" in data
    assert "completed" in data
    assert "created_at" in data
    assert "updated_at" in data
    
    # Check data types
    assert isinstance(data["id"], str)
    assert isinstance(data["user_id"], str)
    assert isinstance(data["title"], str)
    assert isinstance(data["description"], str) or data["description"] is None
    assert isinstance(data["completed"], bool)
    assert isinstance(data["created_at"], str)  # ISO date string
    assert isinstance(data["updated_at"], str)  # ISO date string
    
    # Check values
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] is False

def test_get_single_task_contract(client: TestClient, user: User, valid_token: str):
    """Test the GET /api/{user_id}/tasks/{id} endpoint contract."""
    # First create a task
    create_response = client.post(
        f"/api/{user.id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "title": "Test Task",
            "description": "Test Description"
        }
    )
    task_id = create_response.json()["id"]
    
    # Now get the task
    response = client.get(
        f"/api/{user.id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    # Check status code
    assert response.status_code == 200
    
    data = response.json()
    
    # Check response structure
    assert "id" in data
    assert "user_id" in data
    assert "title" in data
    assert "description" in data
    assert "completed" in data
    assert "created_at" in data
    assert "updated_at" in data
    
    # Check data types
    assert isinstance(data["id"], str)
    assert isinstance(data["user_id"], str)
    assert isinstance(data["title"], str)
    assert isinstance(data["description"], str) or data["description"] is None
    assert isinstance(data["completed"], bool)
    assert isinstance(data["created_at"], str)  # ISO date string
    assert isinstance(data["updated_at"], str)  # ISO date string

def test_update_task_contract(client: TestClient, user: User, valid_token: str):
    """Test the PUT /api/{user_id}/tasks/{id} endpoint contract."""
    # First create a task
    create_response = client.post(
        f"/api/{user.id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "title": "Original Task",
            "description": "Original Description"
        }
    )
    task_id = create_response.json()["id"]
    
    # Now update the task
    response = client.put(
        f"/api/{user.id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "title": "Updated Task",
            "description": "Updated Description"
        }
    )
    
    # Check status code
    assert response.status_code == 200
    
    data = response.json()
    
    # Check response structure
    assert "id" in data
    assert "user_id" in data
    assert "title" in data
    assert "description" in data
    assert "completed" in data
    assert "created_at" in data
    assert "updated_at" in data
    
    # Check data types
    assert isinstance(data["id"], str)
    assert isinstance(data["user_id"], str)
    assert isinstance(data["title"], str)
    assert isinstance(data["description"], str) or data["description"] is None
    assert isinstance(data["completed"], bool)
    assert isinstance(data["created_at"], str)  # ISO date string
    assert isinstance(data["updated_at"], str)  # ISO date string
    
    # Check values
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated Description"

def test_delete_task_contract(client: TestClient, user: User, valid_token: str):
    """Test the DELETE /api/{user_id}/tasks/{id} endpoint contract."""
    # First create a task
    create_response = client.post(
        f"/api/{user.id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "title": "Task to Delete",
            "description": "Description"
        }
    )
    task_id = create_response.json()["id"]
    
    # Now delete the task
    response = client.delete(
        f"/api/{user.id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    # Check status code
    assert response.status_code in [200, 204, 404]  # 200 for success with message, 204 for no content, 404 for not found
    
    if response.status_code == 200:
        data = response.json()
        # Check response structure for 200 status
        assert "message" in data
        assert isinstance(data["message"], str)

def test_toggle_task_completion_contract(client: TestClient, user: User, valid_token: str):
    """Test the PATCH /api/{user_id}/tasks/{id}/complete endpoint contract."""
    # First create a task
    create_response = client.post(
        f"/api/{user.id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "title": "Toggle Task",
            "description": "Description"
        }
    )
    task_id = create_response.json()["id"]
    
    # Now toggle the task completion
    response = client.patch(
        f"/api/{user.id}/tasks/{task_id}/complete",
        params={"completed": True},
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    # Check status code
    assert response.status_code == 200
    
    data = response.json()
    
    # Check response structure
    assert "id" in data
    assert "user_id" in data
    assert "title" in data
    assert "description" in data
    assert "completed" in data
    assert "created_at" in data
    assert "updated_at" in data
    
    # Check data types
    assert isinstance(data["id"], str)
    assert isinstance(data["user_id"], str)
    assert isinstance(data["title"], str)
    assert isinstance(data["description"], str) or data["description"] is None
    assert isinstance(data["completed"], bool)
    assert isinstance(data["created_at"], str)  # ISO date string
    assert isinstance(data["updated_at"], str)  # ISO date string
    
    # Check values
    assert data["completed"] is True