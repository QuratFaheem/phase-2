from sqlmodel import Session, select
from ..models.user import User, UserCreate
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
import uuid
from jose import JWTError, jwt

# Secret key for JWT (in production, use a strong secret from environment)
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    # Ensure both passwords are bytes
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')

    return bcrypt.checkpw(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password, ensuring it doesn't exceed bcrypt's 72-byte limit."""
    # Ensure the password is properly encoded as bytes and within bcrypt limits
    if isinstance(password, str):
        password_bytes = password.encode('utf-8')
    else:
        password_bytes = password

    # Ensure password is not empty
    if not password_bytes:
        raise ValueError("Password cannot be empty")

    # Truncate to 72 bytes to comply with bcrypt limitations
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]

    try:
        # Generate salt and hash the password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        # Return as string
        return hashed.decode('utf-8')
    except Exception as e:
        # Log the error for debugging
        print(f"Error hashing password: {str(e)}")
        # Re-raise with a more generic message
        raise ValueError(f"Password processing error: {str(e)}")

def create_user(user_data: UserCreate, db_session: Session) -> User:
    """Create a new user with hashed password."""
    # Check if user with email already exists
    existing_user = db_session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise ValueError("Email already registered")

    # Hash the password
    hashed_password = get_password_hash(user_data.password)

    # Create the user object
    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_password
    )

    # Add to database
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user

def authenticate_user(email: str, password: str, db_session: Session) -> Optional[User]:
    """Authenticate a user by email and password."""
    user = db_session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt