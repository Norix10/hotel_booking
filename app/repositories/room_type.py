from uuid import UUID
from typing import TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.repositories.base import BaseRepository
from app.models.room_type import RoomType    


class RoomTypeRepository(BaseRepository[RoomType]):
    def __init__(self, session: AsyncSession):
        super().__init__(RoomType, session)