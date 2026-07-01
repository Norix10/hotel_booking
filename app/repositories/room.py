from uuid import UUID
from typing import TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.repositories.base import BaseRepository
from app.models.room import Room
from app.models.enums.room_enum import RoomBathroomTypeEnum, RoomStatusTypeEnum


class RoomRepository(BaseRepository[Room]):
    def __init__(self, session: AsyncSession):
        super().__init__(Room, session)

    async def get_with_type(self, room_id: int) -> Room | None:
        query = (
            select(Room).where(Room.id == room_id).options(joinedload(Room.room_types))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_availble_rooms(self, skip: int = 0, limit: int = 10) -> list[Room]:
        rooms = await self.session.execute(
            select(Room)
            .where(Room.status == RoomStatusTypeEnum.available)
            .offset(skip)
            .limit(limit)
        )
        return rooms.scalars().all()

    async def get_by_id(self, room_id: int) -> Room:
        room = await self.session.execute(select(Room).where(Room.id == room_id))
        return room.scalar_one_or_none()
