import pytest
from fastapi.testclient import TestClient
from main import app
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from models.user import User
from models.task import Task
from services.auth_service import get_password_hash
import uuid
from datetime import datetime

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
    # In a real test, you would generate a valid JWT token
    # For this example, we'll just return a placeholder
    # The actual implementation would use the same token creation logic as in the auth module
    from middleware.jwt_auth import create_access_token
    from datetime import timedelta
    
    access_token_expires = timedelta(minutes=30)
    token_data = {"sub": str(user.id)}
    token = create_access_token(data=token_data, expires_delta=access_token_expires)
    return token

def test_create_task(client: TestClient, user: User, valid_token: str):
    response = client.post(
        f"/api/{user.id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Test Task", "description": "Test Description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] is False

def test_get_tasks(client: TestClient, user: User, valid_token: str):
    # Create a task first
    client.post(
        f"/api/{user.id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Test Task", "description": "Test Description"}
    )
    
    response = client.get(
        f"/api/{user.id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(task["title"] == "Test Task" for task in data)

def test_get_single_task(client: TestClient, user: User, valid_token: str):
    # Create a task first
    create_response = client.post(
        f"/api/{user.id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Test Task", "description": "Test Description"}
    )
    task_id = create_response.json()["id"]
    
    response = client.get(
        f"/api/{user.id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"

def test_update_task(client: TestClient, user: User, valid_token: str):
    # Create a task first
    create_response = client.post(
        f"/api/{user.id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Original Task", "description": "Original Description"}
    )
    task_id = create_response.json()["id"]
    
    response = client.put(
        f"/api/{user.id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Updated Task", "description": "Updated Description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated Description"

def test_delete_task(client: TestClient, user: User, valid_token: str):
    # Create a task first
    create_response = client.post(
        f"/api/{user.id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Task to Delete", "description": "Description"}
    )
    task_id = create_response.json()["id"]
    
    response = client.delete(
        f"/api/{user.id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200
    
    # Verify the task is gone
    get_response = client.get(
        f"/api/{user.id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert get_response.status_code == 404

def test_toggle_task_completion(client: TestClient, user: User, valid_token: str):
    # Create a task first
    create_response = client.post(
        f"/api/{user.id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Toggle Task", "description": "Description"}
    )
    task_id = create_response.json()["id"]
    
    # Toggle to completed
    response = client.patch(
        f"/api/{user.id}/tasks/{task_id}/complete",
        params={"completed": True},
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True
    
    # Toggle back to not completed
    response = client.patch(
        f"/api/{user.id}/tasks/{task_id}/complete",
        params={"completed": False},
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is False

def test_unauthorized_access(client: TestClient, user: User, valid_token: str):
    # Create a task with the valid user
    create_response = client.post(
        f"/api/{user.id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Protected Task", "description": "Description"}
    )
    task_id = create_response.json()["id"]
    
    # Try to access with an invalid token
    invalid_token = "invalid_token"
    response = client.get(
        f"/api/{user.id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {invalid_token}"}
    )
    assert response.status_code == 401