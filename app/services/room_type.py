from fastapi import HTTPException, status

from app.repositories.room_type import RoomTypeRepository
from app.schemas.room_type import (
    RoomTypeCreateSchema,
    RoomTypeResposeSchema,
    RoomTypeUpdateSchema,
)
from app.models.room_type import RoomType


class RoomTypesService:
    def __init__(self, room_types_repo: RoomTypeRepository):
        self.room_types_repo = room_types_repo

    async def _get_room_type_or_404(self, room_type_id: int) -> RoomTypeResposeSchema:
        room_type = await self.room_types_repo.get_by_id(room_type_id)
        if not room_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Room_type is not found"
            )
        return room_type

    async def get_all(
        self, skip: int = 0, limit: int = 100
    ) -> list[RoomTypeResposeSchema]:
        return await self.room_types_repo.get_all(skip=skip, limit=limit)

    async def create_room_type(
        self, data: RoomTypeCreateSchema
    ) -> RoomTypeResposeSchema:
        room_type = RoomType(
            name=data.name,
            base_price=data.base_price,
            capacity=data.capacity,
            bed_type=data.bed_type,
            bathroom_type=data.bathroom_type,
            area_sq_m=data.area_sq_m,
            has_ac=data.has_ac,
            has_wifi=data.has_wifi,
        )
        return await self.room_types_repo.create(room_type)

    async def update_room_type(
        self, room_type_int: int, room_type_data: RoomTypeUpdateSchema
    ) -> RoomTypeResposeSchema:
        room_type = await self._get_room_type_or_404(room_type_int)

        for field, value in room_type_data.model_dump(exclude_unset=True).items():
            setattr(room_type, field, value)

        updated_room_type = await self.room_types_repo.update(room_type)
        return RoomTypeResposeSchema.model_validate(updated_room_type)

    async def delete_room_type(self, room_type_id: int):
        room_type = await self._get_room_type_or_404(room_type_id)
        return await self.room_types_repo.delete(room_type)
