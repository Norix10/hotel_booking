from fastapi import HTTPException, status

from app.repositories.booking import BookingRepository
from app.repositories.payment import PaymentRepository
from app.repositories.room import RoomRepository

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
    ):
        self.booking_repo = booking_repo
        self.payment_repo = payment_repo
        self.room_repo = room_repo

    async def create_booking_with_payment(
        self, user_id: UUID, data: BookingWithPaymentCreateSchema
    ) -> BookingResponseSchema:
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
            user_id=user_id,
            room_id=data.room_id,
            check_in=data.check_in,
            check_out=data.check_out,
            status=BookingStatusEnum.pending,
        )
        new_booking = await self.booking_repo.create(new_booking)

        new_payment = Payment(
            booking_id=new_booking.id,
            amount=data.amount,
            payment_method=data.payment_method,
            payment_status=PaymentStatusEnum.success,
        )
        await self.payment_repo.create(new_payment)
        return BookingResponseSchema.model_validate(new_booking)
