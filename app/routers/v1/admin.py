from uuid import UUID
from fastapi import APIRouter, Depends, Security, status

from app.schemas.booking import BookingResponseSchema, BookingAdminUpdateSchema
from app.schemas.payments import PaymentResponseSchema, PaymentUpdateSchema
from app.core.dependencies import (
    get_current_admin,
    get_booking_service,
    get_payment_service,
)
from app.models.user import User
from app.services.booking import BookingService
from app.services.payments import PaymentsService

router = APIRouter(prefix="/admin", tags=["admin"])


@router.patch("/bookings/{booking_id}", response_model=BookingResponseSchema)
async def admin_update_booking(
    booking_id: UUID,
    data: BookingAdminUpdateSchema,
    current_admin: User = Security(get_current_admin),
    booking_service: BookingService = Depends(get_booking_service),
) -> BookingResponseSchema:
    return await booking_service.admin_update_booking(booking_id, data)


@router.delete("/bookings/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_booking(
    booking_id: UUID,
    current_admin: User = Security(get_current_admin),
    booking_service: BookingService = Depends(get_booking_service),
):
    await booking_service.admin_delete_booking(booking_id)


@router.patch("/payments/{payment_id}", response_model=PaymentResponseSchema)
async def admin_update_payment(
    payment_id: UUID,
    data: PaymentUpdateSchema,
    current_admin: User = Security(get_current_admin),
    payment_service: PaymentsService = Depends(get_payment_service),
) -> PaymentResponseSchema:
    return await payment_service.update_payment(payment_id, data)


@router.delete("/payments/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_payment(
    payment_id: UUID,
    current_admin: User = Security(get_current_admin),
    payment_service: PaymentsService = Depends(get_payment_service),
):
    await payment_service.delete_payment(payment_id)
