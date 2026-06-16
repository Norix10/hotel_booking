from uuid import UUID
from typing import Optional
from fastapi import HTTPException, status
from datetime import datetime

from app.repositories.booking import BookingRepository
from app.repositories.room import RoomRepository
from app.repositories.payment import PaymentRepository

from app.schemas.booking import (
    BookingCreateSchema,
    BookingUpdateSchema,
    BookingAdminUpdateSchema,
    BookingResponseSchema,
    BookingAdminFilterSchema,
)
from app.models.booking import Booking
from app.models.enums.booking_enum import BookingStatusEnum
from app.models.enums.room_enum import RoomStatusTypeEnum


class BookingService:
    def __init__(
        self,
        booking_repo: BookingRepository,
        room_repo: RoomRepository,
        payment_repo: PaymentRepository,
    ):
        self.booking_repo = booking_repo
        self.room_repo = room_repo
        self.payment_repo = payment_repo

    async def _get_booking_or_404(self, booking_id: UUID):
        booking = await self.booking_repo.get_by_id(booking_id)
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found"
            )
        return booking

    async def _get_user_booking_or_404(
        self, user_id: UUID, booking_id: UUID
    ) -> Booking:
        booking = await self.booking_repo.get_user_booking_by_booking_id(
            user_id, booking_id
        )
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found",
            )
        return booking

    async def booking_time_validator(
        self,
        room_id: int,
        check_in: datetime,
        check_out: datetime,
        exclude_booking_id: Optional[UUID] = None,
    ):
        room = await self.room_repo.get_by_id(room_id)
        if room is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
            )
        if room.status != RoomStatusTypeEnum.available:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This room is not available",
            )

        is_overlapping = await self.booking_repo.check_room_overlap(
            room_id, check_in, check_out, exclude_booking_id
        )

        if is_overlapping:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="These dates are already booked",
            )

    async def _update_booking_status_internal(
        self, user_id: UUID, booking_id: UUID, booking_status: BookingStatusEnum
    ) -> BookingResponseSchema:
        booking = await self._get_user_booking_or_404(user_id, booking_id)
        booking.status = booking_status
        updated_booking = await self.booking_repo.update(booking)
        return BookingResponseSchema.model_validate(updated_booking)

    # -----------------------------------------------

    async def get_user_booking_by_id(
        self, user_id: UUID, booking_id: UUID
    ) -> BookingResponseSchema:
        booking = await self.booking_repo.get_user_booking_by_booking_id(
            user_id, booking_id
        )
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found",
            )
        return BookingResponseSchema.model_validate(booking)

    async def admin_get_booking_by_id(self, booking_id: UUID) -> BookingResponseSchema:
        booking = await self._get_booking_or_404(booking_id)
        return BookingResponseSchema.model_validate(booking)

    async def get_all_user_bookings(
        self,
        user_id: UUID,
        status: Optional[BookingStatusEnum] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[BookingResponseSchema]:
        bookings = await self.booking_repo.get_by_user_id(user_id, status, skip, limit)
        return [BookingResponseSchema.model_validate(booking) for booking in bookings]

    async def admin_get_all_bookings(
        self,
        filters: Optional[BookingAdminFilterSchema] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[BookingResponseSchema]:
        bookings = await self.booking_repo.get_all_bookings(filters, skip, limit)
        return [BookingResponseSchema.model_validate(booking) for booking in bookings]

    async def create_booking(
        self, user_id: UUID, data: BookingCreateSchema
    ) -> BookingResponseSchema:
        await self.booking_time_validator(
            room_id=data.room_id, check_in=data.check_in, check_out=data.check_out
        )

        new_booking = Booking(
            user_id=user_id,
            room_id=data.room_id,
            check_in=data.check_in,
            check_out=data.check_out,
            status=BookingStatusEnum.pending,
        )
        new_booking = await self.booking_repo.create(new_booking)

        return BookingResponseSchema.model_validate(new_booking)

    async def update_booking(
        self, user_id: UUID, booking_id: UUID, data: BookingUpdateSchema
    ) -> BookingResponseSchema:
        booking = await self._get_user_booking_or_404(user_id, booking_id)
        room_id = booking.room_id
        check_in = data.check_in if data.check_in is not None else booking.check_in
        check_out = data.check_out if data.check_out is not None else booking.check_out

        await self.booking_time_validator(
            room_id=room_id,
            check_in=check_in,
            check_out=check_out,
            exclude_booking_id=booking_id,
        )

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(booking, field, value)

        updated_booking = await self.booking_repo.update(booking)
        return BookingResponseSchema.model_validate(updated_booking)

    async def admin_update_booking(
        self, booking_id: UUID, data: BookingAdminUpdateSchema
    ) -> BookingResponseSchema:
        booking = await self._get_booking_or_404(booking_id)
        room_id = data.room_id if data.room_id is not None else booking.room_id
        check_in = data.check_in if data.check_in is not None else booking.check_in
        check_out = data.check_out if data.check_out is not None else booking.check_out

        await self.booking_time_validator(
            room_id=room_id,
            check_in=check_in,
            check_out=check_out,
            exclude_booking_id=booking_id,
        )

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(booking, field, value)

        updated_booking = await self.booking_repo.update(booking)
        return BookingResponseSchema.model_validate(updated_booking)

    async def confirm_booking(
        self, user_id: UUID, booking_id: UUID
    ) -> BookingResponseSchema:
        return await self._update_booking_status_internal(
            user_id, booking_id, BookingStatusEnum.confirmed
        )

    async def cancel_booking(
        self, user_id: UUID, booking_id: UUID
    ) -> BookingResponseSchema:
        return await self._update_booking_status_internal(
            user_id, booking_id, BookingStatusEnum.cancelled
        )

    async def admin_delete_booking(self, booking_id: UUID):
        booking = await self._get_booking_or_404(booking_id)
        await self.booking_repo.delete(booking)
