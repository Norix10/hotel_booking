from uuid import UUID
from typing import Optional
from datetime import datetime, timedelta, date
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.repositories.base import BaseRepository
from app.schemas.booking import BookingAdminFilterSchema
from app.models.enums.booking_enum import BookingStatusEnum
from app.models.booking import Booking
from app.models.room import Room


class BookingRepository(BaseRepository[Booking]):
    def __init__(self, session: AsyncSession):
        super().__init__(Booking, session)

    async def get_expired_pending_bookins(self, expiration_minutes: int):
        time = datetime.utcnow() - timedelta(minutes=expiration_minutes)
        query = select(Booking).where(
            Booking.status == BookingStatusEnum.pending, Booking.created_at <= time
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_bookings_for_date(self, target_date: date):
        query = select(Booking).where(
            Booking.status == BookingStatusEnum.confirmed,
            Booking.check_in == target_date,
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_with_room_and_type(self, booking_id: UUID) -> Booking | None:
        query = (
            select(Booking)
            .where(Booking.id == booking_id)
            .options(joinedload(Booking.room).joinedload(Room.room_types))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def check_room_overlap(
        self,
        room_id: int,
        check_in: datetime,
        check_out: datetime,
        exclude_booking_id: Optional[UUID] = None,
    ) -> bool:
        query = select(Booking).where(
            Booking.room_id == room_id,
            Booking.status != BookingStatusEnum.cancelled,
            and_(check_in < Booking.check_out, check_out > Booking.check_in),
        )

        if exclude_booking_id is not None:
            query = query.where(Booking.id != exclude_booking_id)

        query = query.limit(1).with_for_update()

        result = await self.session.execute(query)
        return result.scalars().first() is not None

    async def get_by_user_id(
        self,
        user_id: UUID,
        status: Optional[BookingStatusEnum] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[Booking]:
        query = select(Booking).where(Booking.user_id == user_id)

        if status is not None:
            query = query.where(Booking.status == status)

        query = query.offset(skip).limit(limit)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_all_bookings(
        self,
        filters: Optional[BookingAdminFilterSchema] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[Booking]:
        query = select(Booking)

        if filters is not None:
            filter_dict = filters.model_dump(exclude_none=True)

        check_in_val = filter_dict.pop("check_in", None)
        check_out_val = filter_dict.pop("check_out", None)

        for field_name, value in filter_dict.items():
            if hasattr(Booking, field_name):
                query = query.where(getattr(Booking, field_name) == value)

        if check_in_val is not None:
            query = query.where(Booking.check_in >= check_in_val)
        if check_out_val is not None:
            query = query.where(Booking.check_out <= check_out_val)

        query = query.offset(skip).limit(limit)

        result = await self.session.execute(query)
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

    async def get_user_booking_by_booking_id(
        self, user_id: UUID, booking_id: UUID
    ) -> Booking:
        result = await self.session.execute(
            select(Booking).where(Booking.user_id == user_id, Booking.id == booking_id)
        )
        return result.scalar_one_or_none()
