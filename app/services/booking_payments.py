from uuid import UUID
from fastapi import HTTPException, status

from app.repositories.booking import BookingRepository
from app.repositories.payment import PaymentRepository
from app.repositories.room import RoomRepository

from app.services.booking import BookingService

from app.schemas.booking import (
    BookingWithPaymentCreateSchema,
    BookingResponseSchema,
)
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.enums.booking_enum import BookingStatusEnum
from app.models.enums.room_enum import RoomStatusTypeEnum
from app.models.enums.payments_enum import PaymentStatusEnum


class BookingPaymentService:
    def __init__(
        self,
        booking_repo: BookingRepository,
        payment_repo: PaymentRepository,
        room_repo: RoomRepository,
        booking_service: BookingService,
    ):
        self.booking_repo = booking_repo
        self.payment_repo = payment_repo
        self.room_repo = room_repo
        self.booking_service = booking_service

    async def create_booking_with_payment(
        self, user_id: UUID, data: BookingWithPaymentCreateSchema
    ) -> BookingResponseSchema:

        await self.booking_service.booking_time_validator(
            data.room_id, data.check_in, data.check_out
        )

        room = await self.room_repo.get_with_type(data.room_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found",
            )
        days = (data.check_out - data.check_in).days
        if days <= 0:
            days = 1
        calculated_amount = days * room.room_types.base_price

        new_booking = Booking(
            user_id=user_id,
            room_id=data.room_id,
            check_in=data.check_in,
            check_out=data.check_out,
            status=BookingStatusEnum.pending,
        )
        new_booking = await self.booking_repo.create(new_booking)

        new_payment = Payment(
            booking_id=new_booking.id,
            user_id=user_id,
            amount=calculated_amount,
            payment_method=data.payment_method,
            payment_status=PaymentStatusEnum.success,
        )
        await self.payment_repo.create(new_payment)
        return BookingResponseSchema.model_validate(new_booking)
