from fastapi import APIRouter, Depends, Security, status

from app.schemas.room_type import (
    RoomTypeResposeSchema,
    RoomTypeCreateSchema,
    RoomTypeUpdateSchema,
)
from app.core.dependencies import (
    get_room_type_service,
    get_current_admin,
)
from app.models.user import User
from app.services.room_type import RoomTypesService

router = APIRouter(prefix="/room-types", tags=["room types"])


@router.post("/", response_model=RoomTypeResposeSchema)
async def create_room_type(
    data: RoomTypeCreateSchema,
    current_admin: User = Security(get_current_admin),
    room_type_service: RoomTypesService = Depends(get_room_type_service),
) -> RoomTypeResposeSchema:
    return await room_type_service.create_room_type(data)


@router.get("/", response_model=list[RoomTypeResposeSchema])
async def get_all_room_types(
    room_type_service: RoomTypesService = Depends(get_room_type_service),
    skip: int = 0,
    limit: int = 100,
):
    return await room_type_service.get_all(skip=skip, limit=limit)


@router.get("/{room_type_id}", response_model=RoomTypeResposeSchema)
async def get_room_type_by_id(
    room_type_id: int,
    room_type_service: RoomTypesService = Depends(get_room_type_service),
) -> RoomTypeResposeSchema:
    return await room_type_service._get_room_type_or_404(room_type_id)


@router.patch("/{room_type_id}", response_model=RoomTypeResposeSchema)
async def update_room_type_by_id(
    room_type_id: int,
    data: RoomTypeUpdateSchema,
    current_admin: User = Security(get_current_admin),
    room_type_service: RoomTypesService = Depends(get_room_type_service),
) -> RoomTypeResposeSchema:
    return await room_type_service.update_room_type(room_type_id, data)


@router.delete("/{room_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room_type_by_id(
    room_type_id: int,
    current_admin: User = Security(get_current_admin),
    room_type_service: RoomTypesService = Depends(get_room_type_service),
):
    await room_type_service.delete_room_type(room_type_id)


@router.delete("/all", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_room_types(
    current_admin: User = Security(get_current_admin),
    room_type_service: RoomTypesService = Depends(get_room_type_service),
):
    await room_type_service.delete_all_room_types()
