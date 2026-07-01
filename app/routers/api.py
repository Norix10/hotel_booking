from fastapi import APIRouter

from app.routers.v1 import (
    user,
    booking,
    payments,
    room,
    room_types,
    admin,
)
from app.routers import health

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health.router)
api_router.include_router(user.router)
api_router.include_router(room_types.router)
api_router.include_router(room.router)
api_router.include_router(booking.router)
api_router.include_router(payments.router)
api_router.include_router(admin.router)
