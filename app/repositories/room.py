from uuid import UUID
from typing import TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.repositories.base import BaseRepository
from app.models.room import Room
from app.models.enums.room_enum import RoomBathroomType, RoomStatusType


class RoomRepository(BaseRepository[Room]):
    def __init__(self, session: AsyncSession):
        super().__init__(Room, session)

    async def get_availble_room(self) -> list[Room]:
        rooms = await self.session.execute(
            select(Room).where(Room.status == RoomStatusType.available)
        )
        return rooms.scalars().all()

    async def get_by_id(self, room_id: int) -> Room:
        room = await self.session.execute(select(Room).where(Room.id == room_id))
        return room.scalar_one_or_none()
