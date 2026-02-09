from fastapi import APIRouter
from .. import tasks, auth

# Create a router for version 1 of the API
v1_router = APIRouter(prefix="/v1")

# Include the existing routes under the v1 prefix
v1_router.include_router(auth.router, tags=["authentication"])
v1_router.include_router(tasks.router, tags=["tasks"])

# This allows us to easily add version-specific middleware or configurations
def get_v1_router():
    return v1_router