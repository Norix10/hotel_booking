from fastapi import APIRouter, Depends, Security, status

from app.schemas.room import (
    RoomResponseSchema,
    RoomCreateSchema,
)
from app.core.dependencies import (
    get_room_service,
)
from app.models.user import User
from app.services.room import RoomService

router = APIRouter(prefix="/room", tags=["room"])


@router.get("/", response_model=list[RoomResponseSchema])
async def get_all_room(
    skip: int = 0,
    limit: int = 10,
    room_service: RoomService = Depends(get_room_service),
):
    return await room_service.get_all_rooms(skip, limit)


@router.get("/available", response_model=list[RoomResponseSchema])
async def get_available_rooms(
    skip: int = 0,
    limit: int = 10,
    room_service: RoomService = Depends(get_room_service),
) -> list[RoomResponseSchema]:
    return await room_service.get_all_rooms(skip, limit)


@router.get("/{room_id}", response_model=RoomResponseSchema)
async def get_room_by_id(
    room_id: int,
    room_service: RoomService = Depends(get_room_service),
):
    return await room_service._get_room_or_404(room_id)
