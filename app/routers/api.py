from fastapi import APIRouter

from app.routers.v1 import (
    user
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user.router)