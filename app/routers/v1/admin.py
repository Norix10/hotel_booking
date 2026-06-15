from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, Security, status, Query

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


@router.get("/bookings/{booking_id}", response_model=BookingResponseSchema)
async def get_booking_by_id(
    booking_id: UUID,
    current_admin: User = Security(get_current_admin),
    booking_service: BookingService = Depends(get_booking_service),
) -> BookingResponseSchema:
    return await booking_service.get_booking_by_id(booking_id)


# @router.get("/bookings/", response_model=list[BookingResponseSchema])
# async def get_bookings(
#     current_admin: User = Security(get_current_admin),
#     booking_service: BookingService = Depends(get_booking_service),
#     filters: Optional[BookingResponseSchema] = Query(...),
#     skip: int = 0,
#     limit: int = 10,
# ) -> list[BookingResponseSchema]:
#     pass


@router.get("/payments/", response_model=list[PaymentResponseSchema])
async def list_payments(
    skip: int = 0,
    limit: int = 10,
    current_admin: User = Security(get_current_admin),
    payment_service: PaymentsService = Depends(get_payment_service),
) -> list[PaymentResponseSchema]:
    return await payment_service.get_all_payments(skip=skip, limit=limit)


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
