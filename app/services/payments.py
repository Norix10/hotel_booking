from uuid import UUID
from fastapi import HTTPException, status

from app.repositories.payment import PaymentRepository
from app.repositories.booking import BookingRepository
from app.schemas.payments import (
    PaymentCreateSchema,
    PaymentResponseSchema,
    PaymentUpdateSchema,
)
from app.models.payment import Payment
from app.models.enums.payments_enum import PaymentStatusEnum
from app.models.enums.booking_enum import BookingStatusEnum


class PaymentsService:
    def __init__(
        self, payment_repo: PaymentRepository, booking_repo: BookingRepository
    ):
        self.payment_repo = payment_repo
        self.booking_repo = booking_repo

    async def _get_payment_or_404(self, payment_id: UUID):
        payment = await self.payment_repo.get_by_id(payment_id)
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found"
            )
        return payment

    async def _get_booking_or_404(self, booking_id: UUID):
        booking = await self.booking_repo.get_by_id(booking_id)
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found"
            )
        return booking

    async def _ensure_booking_has_no_payment(self, booking_id: UUID):
        payment = await self.payment_repo.get_by_booking_id(booking_id)
        if payment:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This booking already has a payment",
            )

    async def create_payment(
        self,
        booking_id: UUID,
        data: PaymentCreateSchema,
        user_id: UUID | None = None,
    ) -> PaymentResponseSchema:
        booking = await self._get_booking_or_404(booking_id)
        if user_id is not None and booking.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot create payment for another user's booking",
            )

        await self._ensure_booking_has_no_payment(booking_id)

        if booking.status == BookingStatusEnum.cancelled:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot create payment for cancelled booking",
            )

        new_payment = Payment(
            booking_id=booking_id,
            amount=data.amount,
            payment_method=data.payment_method,
            payment_status=PaymentStatusEnum.pending,
        )
        new_payment = await self.payment_repo.create(new_payment)
        return PaymentResponseSchema.model_validate(new_payment)

    async def get_payment_by_id(self, payment_id: UUID) -> PaymentResponseSchema:
        payment = await self._get_payment_or_404(payment_id)
        return PaymentResponseSchema.model_validate(payment)

    async def get_all_payments(
        self, skip: int = 0, limit: int = 100
    ) -> list[PaymentResponseSchema]:
        payments = await self.payment_repo.get_all(skip=skip, limit=limit)
        return [PaymentResponseSchema.model_validate(payment) for payment in payments]

    async def update_payment(
        self, payment_id: UUID, data: PaymentUpdateSchema
    ) -> PaymentResponseSchema:
        payment = await self._get_payment_or_404(payment_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(payment, field, value)

        updated_payment = await self.payment_repo.update(payment)
        return PaymentResponseSchema.model_validate(updated_payment)

    async def delete_payment(self, payment_id: UUID):
        payment = await self._get_payment_or_404(payment_id)
        await self.payment_repo.delete(payment)
