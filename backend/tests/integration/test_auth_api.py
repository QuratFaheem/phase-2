import pytest
from fastapi.testclient import TestClient
from main import app
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from models.user import User
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
    from middleware.jwt_auth import create_access_token
    from datetime import timedelta
    
    access_token_expires = timedelta(minutes=30)
    token_data = {"sub": str(user.id)}
    token = create_access_token(data=token_data, expires_delta=access_token_expires)
    return token

def test_successful_authentication(client: TestClient, user: User):
    """Test that a user can successfully authenticate."""
    response = client.post(
        "/auth/signin",
        json={
            "email": "testuser@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_failed_authentication_invalid_credentials(client: TestClient):
    """Test that authentication fails with invalid credentials."""
    response = client.post(
        "/auth/signin",
        json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    data = response.json()
    assert "Incorrect email or password" in data["detail"]

def test_failed_authentication_missing_fields(client: TestClient):
    """Test that authentication fails with missing fields."""
    response = client.post(
        "/auth/signin",
        json={
            "email": "testuser@example.com"
            # Missing password
        }
    )
    assert response.status_code == 422  # Validation error

def test_protected_route_with_valid_token(client: TestClient, user: User, valid_token: str):
    """Test that a protected route works with a valid token."""
    # Create a task to test with
    create_response = client.post(
        f"/api/{user.id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Test Task", "description": "Test Description"}
    )
    assert create_response.status_code == 200
    
    # Get the tasks
    response = client.get(
        f"/api/{user.id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200

def test_protected_route_without_token(client: TestClient, user: User):
    """Test that a protected route fails without a token."""
    response = client.get(f"/api/{user.id}/tasks")
    assert response.status_code == 403  # Not authorized

def test_protected_route_with_invalid_token(client: TestClient, user: User):
    """Test that a protected route fails with an invalid token."""
    response = client.get(
        f"/api/{user.id}/tasks",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401  # Could not validate credentials

def test_cross_user_access_prevention(client: TestClient, session: Session, user: User, valid_token: str):
    """Test that a user cannot access another user's resources."""
    # Create another user
    other_user = User(
        id=uuid.uuid4(),
        email="otheruser@example.com",
        hashed_password=get_password_hash("otherpassword"),
        name="Other User",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(other_user)
    session.commit()
    session.refresh(other_user)
    
    # Create a task for the other user
    other_user_token_data = {"sub": str(other_user.id)}
    from middleware.jwt_auth import create_access_token
    from datetime import timedelta
    access_token_expires = timedelta(minutes=30)
    other_user_token = create_access_token(data=other_user_token_data, expires_delta=access_token_expires)
    
    create_response = client.post(
        f"/api/{other_user.id}/tasks",
        headers={"Authorization": f"Bearer {other_user_token}"},
        json={"title": "Other User's Task", "description": "Private task"}
    )
    assert create_response.status_code == 200
    task_data = create_response.json()
    task_id = task_data["id"]
    
    # Try to access other user's task with current user's token
    response = client.get(
        f"/api/{other_user.id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 403  # Not authorized to access these tasks

def test_user_registration_success(client: TestClient):
    """Test that a user can successfully register."""
    response = client.post(
        "/auth/signup",
        json={
            "email": "newuser@example.com",
            "password": "newpassword123",
            "name": "New User"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["name"] == "New User"

def test_user_registration_duplicate_email(client: TestClient, user: User):
    """Test that registration fails with duplicate email."""
    response = client.post(
        "/auth/signup",
        json={
            "email": "testuser@example.com",  # Existing email
            "password": "newpassword123",
            "name": "Another User"
        }
    )
    assert response.status_code == 409  # Conflict - email already registered