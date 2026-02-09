from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
from datetime import datetime, timedelta
from typing import Optional
import jwt
import hashlib
import os

router = APIRouter()

# Secret key for JWT (should be moved to environment variables in production)
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-here-for-development-only")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class User(BaseModel):
    id: Optional[str] = None
    email: str
    name: Optional[str] = None

class UserCreate(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# In-memory storage for development (replace with database in production)
fake_users_db = {}

def verify_password(plain_password, hashed_password):
    # Simple SHA256 hashing for demo purposes (not recommended for production)
    return get_password_hash(plain_password) == hashed_password

def get_password_hash(password):
    # Simple SHA256 hashing for demo purposes (not recommended for production)
    return hashlib.sha256(password.encode()).hexdigest()

def get_user(email: str):
    if email in fake_users_db:
        user_data = fake_users_db[email]
        return User(id=user_data["id"], email=user_data["email"], name=user_data.get("name"))
    return None

def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, fake_users_db[email]["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/auth/signup", response_model=Token)
async def signup(user_create: UserCreate):
    try:
        # Check if user already exists
        if get_user(user_create.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        hashed_password = get_password_hash(user_create.password)
        user_id = str(uuid.uuid4())
        
        fake_users_db[user_create.email] = {
            "id": user_id,
            "email": user_create.email,
            "name": user_create.name,
            "hashed_password": hashed_password
        }
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_create.email}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(f"Signup error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/auth/signin", response_model=Token)
async def signin(user_login: UserLogin):
    try:
        user = authenticate_user(user_login.email, user_login.password)
        if not user:
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_login.email}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(f"Signin error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")