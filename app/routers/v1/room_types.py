from fastapi import APIRouter, Depends

from app.schemas.room_type import (
    RoomTypeResposeSchema,
    RoomTypeFilterSchema,
)
from app.core.dependencies import (
    get_room_type_service,
    get_current_admin,
)
from app.services.room_type import RoomTypesService

router = APIRouter(prefix="/room-types", tags=["room types"])


@router.get("/", response_model=list[RoomTypeResposeSchema])
async def get_all_room_types(
    room_type_service: RoomTypesService = Depends(get_room_type_service),
    filters: RoomTypeFilterSchema = Depends(),
    skip: int = 0,
    limit: int = 10,
):
    return await room_type_service.get_all_room_types(filters, skip, limit)


@router.get("/{room_type_id}", response_model=RoomTypeResposeSchema)
async def get_room_type_by_id(
    room_type_id: int,
    room_type_service: RoomTypesService = Depends(get_room_type_service),
) -> RoomTypeResposeSchema:
    return await room_type_service._get_room_type_or_404(room_type_id)
