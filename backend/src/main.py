from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.auth import router as auth_router
from src.api.tasks import router as tasks_router
from src.api.chat import router as chat_router

# Create the FastAPI app with custom metadata for documentation
app = FastAPI(
    title="Todo API",
    description="A secure, multi-user todo application with persistent storage and AI chatbot integration",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the auth router
app.include_router(auth_router, prefix="", tags=["authentication"])
# Include the tasks router
app.include_router(tasks_router, tags=["tasks"])
# Include the chat router
app.include_router(chat_router, tags=["chat"])

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to the Todo API. Visit /docs for API documentation."}

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)