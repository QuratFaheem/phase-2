from sqlmodel import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)