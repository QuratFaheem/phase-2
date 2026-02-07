from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Annotated
from ..database.connection import engine
from ..models.user import User, UserCreate, UserRead, UserLogin
from ..services.auth_service import create_user, authenticate_user, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/signup")
def signup(user_data: UserCreate, session: Annotated[Session, Depends(get_session)]):
    """Register a new user and return an access token."""
    try:
        user = create_user(user_data, session)

        # Create access token for the newly registered user
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": str(user.id)}, expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "created_at": user.created_at
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/signin")
def signin(user_data: UserLogin, session: Annotated[Session, Depends(get_session)]):
    """Authenticate a user and return an access token."""
    user = authenticate_user(user_data.email, user_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": str(user.id)}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at
        }
    }