from fastapi import APIRouter, Depends, Security, status

from app.schemas.room import (
    RoomResponseSchema,
    RoomCreateSchema,
    RoomUpdateSchema,
)
from app.core.dependencies import (
    get_room_service,
    get_current_admin,
)
from app.models.user import User
from app.services.room import RoomService

router = APIRouter(prefix="/room", tags=["room"])


@router.post("/", response_model=RoomResponseSchema)
async def create_room(
    data: RoomCreateSchema,
    current_admin: User = Security(get_current_admin),
    room_service: RoomService = Depends(get_room_service),
):
    return await room_service.create_room(data)


@router.get("/{room_id}", response_model=RoomResponseSchema)
async def get_room_by_id(
    room_id: int,
    room_service: RoomService = Depends(get_room_service),
):
    return await room_service._get_room_or_404(room_id)


@router.get("/", response_model=list[RoomResponseSchema])
async def get_all_room(
    skip: int = 0,
    limit: int = 10,
    room_service: RoomService = Depends(get_room_service),
):
    return await room_service.get_all_rooms(skip, limit)


@router.patch("/{room_id}", response_model=RoomResponseSchema)
async def update_room(
    room_id: int,
    data: RoomUpdateSchema,
    current_admin: User = Security(get_current_admin),
    room_service: RoomService = Depends(get_room_service),
):
    return await room_service.update_room(room_id, data)


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    room_id: int,
    current_admin: User = Security(get_current_admin),
    room_service: RoomService = Depends(get_room_service),
):
    await room_service.delete_room(room_id)
