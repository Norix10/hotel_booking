from uuid import UUID
from fastapi import HTTPException, status

from app.repositories.booking import BookingRepository
from app.repositories.room import RoomRepository
from app.repositories.payment import PaymentRepository

from app.schemas.booking import (
    BookingCreateSchema,
    BookingWithPaymentCreateSchema,
    BookingUpdateSchema,
    BookingAdminUpdateSchema,
    BookingResponseSchema,
)
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.enums.booking_enum import BookingStatusEnum
from app.models.enums.room_enum import RoomStatusTypeEnum
from app.models.enums.payments_enum import PaymentStatusEnum


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

    async def _update_booking_internal(
        self, booking_id: UUID, data
    ) -> BookingResponseSchema:
        booking = await self._get_booking_or_404(booking_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(booking, field, value)

        updated_booking = await self.booking_repo.update(booking)
        return BookingResponseSchema.model_validate(updated_booking)

    async def create_booking(self, data: BookingCreateSchema) -> BookingResponseSchema:
        room = await self.room_repo.get_by_id(data.room_id)
        if room is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
            )

        if room.status != RoomStatusTypeEnum.available:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This room is not available",
            )

        existing_bookings = await self.booking_repo.get_by_room_id(data.room_id)
        for booking in existing_bookings:
            if data.check_in < booking.check_out and data.check_out > booking.check_in:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="These dates are already booked",
                )

        new_booking = Booking(
            user_id=data.user_id,
            room_id=data.room_id,
            check_in=data.check_in,
            check_out=data.check_out,
            status=BookingStatusEnum.pending,
        )
        new_booking = await self.booking_repo.create(new_booking)

        return BookingResponseSchema.model_validate(new_booking)

    async def get_all_bookings(
        self, skip: int = 0, limit: int = 100
    ) -> list[BookingResponseSchema]:
        return await self.booking_repo.get_all(skip=skip, limit=limit)

    async def update_booking(
        self, booking_id: UUID, data: BookingUpdateSchema
    ) -> BookingResponseSchema:
        return await self._update_booking_internal(booking_id, data)

    async def admin_update_booking(
        self, booking_id: UUID, data: BookingAdminUpdateSchema
    ) -> BookingResponseSchema:
        return await self._update_booking_internal(booking_id, data)

    async def cancel_booking(self, booking_id: UUID) -> BookingResponseSchema:
        booking = await self._get_booking_or_404(booking_id)
        booking.status = BookingStatusEnum.cancelled
        updated_booking = await self.booking_repo.update(booking)
        return BookingResponseSchema.model_validate(updated_booking)

    async def delete_booking(self, booking_id: UUID):
        booking = await self._get_booking_or_404(booking_id)
        return await self.booking_repo.delete(booking)
