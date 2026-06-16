from uuid import UUID
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.repositories.base import BaseRepository
from app.schemas.room_type import RoomTypeFilterSchema
from app.models.room_type import RoomType


class RoomTypeRepository(BaseRepository[RoomType]):
    def __init__(self, session: AsyncSession):
        super().__init__(RoomType, session)

    async def get_by_id(self, id: int) -> RoomType | None:
        result = await self.session.execute(select(RoomType).where(RoomType.id == id))
        return result.scalar_one_or_none()

    async def get_room_types(
        self,
        filters: Optional[RoomTypeFilterSchema] = None,
        skip: int = 0,
        limit: int = 10,
    ):
        query = select(RoomType)

        if filters is not None:
            filter_dict = filters.model_dump(exclude_none=True)
            for field_name, value in filter_dict.items():
                if hasattr(RoomType, field_name):
                    query = query.where(getattr(RoomType, field_name) == value)

        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())
