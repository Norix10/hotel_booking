from fastapi import HTTPException, status

from app.repositories.room import RoomRepository
from app.schemas.room import RoomResponseSchema, RoomCreateSchema, RoomUpdateSchema
from app.models.room import Room


class RoomService:
    def __init__(self, room_repo: RoomRepository):
        self.room_repo = room_repo

    async def get_all_rooms(
        self, skip: int = 0, limit: int = 10
    ) -> list[RoomResponseSchema]:
        return await self.room_repo.get_all(skip, limit)

    async def _get_room_or_404(self, room_id: int) -> RoomResponseSchema:
        room = await self.room_repo.get_by_id(room_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
            )
        return room

    async def create_room(self, data: RoomCreateSchema) -> RoomResponseSchema:
        room = Room(
            room_name=data.room_name,
            room_type_id=data.room_type_id,
            status=data.status,
            floor=data.floor,
        )
        return await self.room_repo.create(room)

    async def update_room(
        self, room_id: int, room_data: RoomUpdateSchema
    ) -> RoomResponseSchema:
        room = await self._get_room_or_404(room_id)

        for field, value in room_data.model_dump(exclude_unset=True).items():
            setattr(room, field, value)

        updated_room = await self.room_repo.update(room)
        return RoomResponseSchema.model_validate(updated_room)

    async def delete_room(self, room_id: int):
        room = await self._get_room_or_404(room_id)
        await self.room_repo.delete(room)
