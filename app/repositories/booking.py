from uuid import UUID
from typing import TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.repositories.base import BaseRepository
from app.models.enums.booking_enum import BookingStatusEnum
from app.models.booking import Booking
from app.models.user import User


class BookingRepository(BaseRepository[Booking]):
    def __init__(self, session: AsyncSession):
        super().__init__(Booking, session)

    async def get_by_user_id(self, user_id: UUID) -> list[Booking]:
        result = await self.session.execute(
            select(Booking).where(Booking.user_id == user_id)
        )
        return result.scalars().all()

    async def get_by_room_id(self, room_id: int) -> list[Booking]:
        result = await self.session.execute(
            select(Booking).where(
                Booking.room_id == room_id,
                Booking.status != BookingStatusEnum.cancelled,
            )
        )
        return result.scalars().all()

    async def get_active_bookings(self) -> list[Booking]:
        result = await self.session.execute(
            select(Booking).where(Booking.status != BookingStatusEnum.cancelled)
        )
        return result.scalars().all()
