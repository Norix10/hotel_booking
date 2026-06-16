from uuid import UUID
from fastapi import APIRouter, Depends, Security, status

from app.schemas.payments import (
    PaymentCreateSchema,
    PaymentResponseSchema,
    PaymentUpdateSchema,
)
from app.core.dependencies import (
    get_payment_service,
    get_current_user,
    get_current_admin,
)
from app.models.user import User
from app.services.payments import PaymentsService

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post(
    "/bookings/{booking_id}",
    response_model=PaymentResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
    booking_id: UUID,
    data: PaymentCreateSchema,
    current_user: User = Security(get_current_user),
    payment_service: PaymentsService = Depends(get_payment_service),
) -> PaymentResponseSchema:
    return await payment_service.create_payment(
        booking_id, data, user_id=current_user.id
    )


@router.get("/", response_model=list[PaymentResponseSchema])
async def get_my_payments(
    current_user: User = Security(get_current_user),
    skip: int = 0,
    limit: int = 10,
    payment_service: PaymentsService = Depends(get_payment_service),
) -> list[PaymentResponseSchema]:
    return await payment_service.get_all_user_payments(current_user.id, skip, limit)


@router.get("/{payment_id}", response_model=PaymentResponseSchema)
async def get_payment(
    payment_id: UUID,
    current_admin: User = Security(get_current_admin),
    payment_service: PaymentsService = Depends(get_payment_service),
) -> PaymentResponseSchema:
    return await payment_service.get_payment_by_id(payment_id)


@router.patch("/{payment_id}", response_model=PaymentResponseSchema)
async def update_payment(
    payment_id: UUID,
    data: PaymentUpdateSchema,
    current_admin: User = Security(get_current_admin),
    payment_service: PaymentsService = Depends(get_payment_service),
) -> PaymentResponseSchema:
    return await payment_service.update_payment(payment_id, data)


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payment(
    payment_id: UUID,
    current_admin: User = Security(get_current_admin),
    payment_service: PaymentsService = Depends(get_payment_service),
):
    await payment_service.delete_payment(payment_id)
