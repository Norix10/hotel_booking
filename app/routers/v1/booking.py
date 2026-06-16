from uuid import UUID
from fastapi import APIRouter, Depends, Security, status, Query
from typing import Optional

from app.schemas.booking import (
    BookingResponseSchema,
    BookingCreateSchema,
    BookingUpdateSchema,
    BookingWithPaymentCreateSchema,
)
from app.core.dependencies import (
    get_booking_service,
    get_booking_payment_service,
    get_current_user,
)
from app.models.user import User
from app.models.enums.booking_enum import BookingStatusEnum
from app.services.booking import BookingService
from app.services.booking_payments import BookingPaymentService

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post(
    "/", response_model=BookingResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_booking(
    data: BookingCreateSchema,
    current_user: User = Security(get_current_user),
    booking_service: BookingService = Depends(get_booking_service),
) -> BookingResponseSchema:
    return await booking_service.create_booking(current_user.id, data)


@router.post(
    "/with-payment",
    response_model=BookingResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_booking_with_payment(
    data: BookingWithPaymentCreateSchema,
    current_user: User = Security(get_current_user),
    booking_payment_service: BookingPaymentService = Depends(
        get_booking_payment_service
    ),
) -> BookingResponseSchema:
    return await booking_payment_service.create_booking_with_payment(
        current_user.id, data
    )


@router.get("/{booking_id}", response_model=BookingResponseSchema)
async def get_booking_by_id(
    booking_id: UUID,
    current_user: User = Security(get_current_user),
    booking_service: BookingService = Depends(get_booking_service),
) -> BookingResponseSchema:
    return await booking_service.get_user_booking_by_id(current_user.id, booking_id)


@router.get("/", response_model=list[BookingResponseSchema])
async def get_my_booking_by_status(
    current_user: User = Security(get_current_user),
    status: Optional[BookingStatusEnum] = Query(None),
    skip: int = 0,
    limit: int = 10,
    booking_service: BookingService = Depends(get_booking_service),
) -> list[BookingResponseSchema]:
    return await booking_service.get_all_user_bookings(
        current_user.id, status, skip, limit
    )


@router.patch("/{booking_id}", response_model=BookingResponseSchema)
async def update_booking(
    booking_id: UUID,
    data: BookingUpdateSchema,
    current_user: User = Security(get_current_user),
    booking_service: BookingService = Depends(get_booking_service),
) -> BookingResponseSchema:
    return await booking_service.update_booking(current_user.id, booking_id, data)


@router.patch("/{booking_id}/confirm", response_model=BookingResponseSchema)
async def confirm_booking(
    booking_id: UUID,
    current_user: User = Security(get_current_user),
    booking_service: BookingService = Depends(get_booking_service),
) -> BookingResponseSchema:
    return await booking_service.confirm_booking(current_user.id, booking_id)


@router.patch("/{booking_id}/cancel", response_model=BookingResponseSchema)
async def cancel_booking(
    booking_id: UUID,
    current_user: User = Security(get_current_user),
    booking_service: BookingService = Depends(get_booking_service),
) -> BookingResponseSchema:
    return await booking_service.cancel_booking(current_user.id, booking_id)
