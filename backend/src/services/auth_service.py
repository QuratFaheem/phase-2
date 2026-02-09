from sqlmodel import Session
from passlib.context import CryptContext
from database.connection import engine
from models.user import User
import uuid
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_user(email: str, password: str, name: str = None) -> User:
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.query(User).filter(User.email == email).first()
        if existing_user:
            return None  # User already exists
        
        # Hash the password
        hashed_password = get_password_hash(password)
        
        # Create new user
        user = User(
            id=uuid.uuid4(),
            email=email,
            hashed_password=hashed_password,
            name=name,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        session.add(user)
        session.commit()
        session.refresh(user)
        
        return user

def authenticate_user(email: str, password: str) -> User:
    with Session(engine) as session:
        user = session.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user