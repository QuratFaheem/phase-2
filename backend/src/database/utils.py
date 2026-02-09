from sqlmodel import Session, select
from database.connection import engine
from models.user import User
from typing import Optional
import uuid


def get_user_by_id(user_id: str) -> Optional[User]:
    """Get a user by their ID."""
    with Session(engine) as session:
        user = session.get(User, uuid.UUID(user_id))
        return user


def get_user_by_email(email: str) -> Optional[User]:
    """Get a user by their email address."""
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        return user


def user_exists(user_id: str) -> bool:
    """Check if a user exists by their ID."""
    user = get_user_by_id(user_id)
    return user is not None


def validate_user_ownership(resource_user_id: str, requesting_user_id: str) -> bool:
    """Validate that the requesting user owns the resource."""
    return resource_user_id == requesting_user_id