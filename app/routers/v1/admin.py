from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, Security, status, Query

from app.schemas.user import UserResponseSchema
from app.schemas.room_type import (
    RoomTypeResposeSchema,
    RoomTypeUpdateSchema,
    RoomTypeCreateSchema,
)
from app.schemas.room import RoomResponseSchema, RoomCreateSchema, RoomUpdateSchema
from app.schemas.booking import (
    BookingResponseSchema,
    BookingAdminUpdateSchema,
    BookingAdminFilterSchema,
)
from app.schemas.payments import PaymentResponseSchema, PaymentUpdateSchema
from app.core.dependencies import (
    get_current_admin,
    get_user_service,
    get_room_type_service,
    get_room_service,
    get_booking_service,
    get_payment_service,
)
from app.models.user import User
from app.services.user import UserService
from app.services.room_type import RoomTypesService
from app.services.room import RoomService
from app.services.booking import BookingService
from app.services.payments import PaymentsService

router = APIRouter(prefix="/admin", tags=["admin"])

# ---------------------------------- USERS ---------------------------------


@router.get("/users/", response_model=list[UserResponseSchema])
async def get_users_list(
    current_admin: User = Security(get_current_admin),
    user_service: UserService = Depends(get_user_service),
) -> list[UserResponseSchema]:
    return await user_service.get_all_users()


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(
    user_id: UUID,
    current_admin: User = Security(get_current_admin),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.delete_user(user_id)


# ---------------------------------- ROOM_TYPES ---------------------------------


@router.post("/room-types/", response_model=RoomTypeResposeSchema)
async def create_room_type(
    data: RoomTypeCreateSchema,
    current_admin: User = Security(get_current_admin),
    room_type_service: RoomTypesService = Depends(get_room_type_service),
) -> RoomTypeResposeSchema:
    return await room_type_service.create_room_type(data)


@router.patch("/room-types/{room_type_id}", response_model=RoomTypeResposeSchema)
async def update_room_type_by_id(
    room_type_id: int,
    data: RoomTypeUpdateSchema,
    current_admin: User = Security(get_current_admin),
    room_type_service: RoomTypesService = Depends(get_room_type_service),
) -> RoomTypeResposeSchema:
    return await room_type_service.update_room_type(room_type_id, data)


@router.delete("/room-types/all", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_room_types(
    current_admin: User = Security(get_current_admin),
    room_type_service: RoomTypesService = Depends(get_room_type_service),
):
    await room_type_service.delete_all_room_types()


@router.delete("/room-types/{room_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room_type_by_id(
    room_type_id: int,
    current_admin: User = Security(get_current_admin),
    room_type_service: RoomTypesService = Depends(get_room_type_service),
):
    await room_type_service.delete_room_type(room_type_id)


# ---------------------------------- ROOM ---------------------------------


@router.post("/room/", response_model=RoomResponseSchema)
async def create_room(
    data: RoomCreateSchema,
    current_admin: User = Security(get_current_admin),
    room_service: RoomService = Depends(get_room_service),
):
    return await room_service.create_room(data)


@router.patch("/room/{room_id}", response_model=RoomResponseSchema)
async def update_room(
    room_id: int,
    data: RoomUpdateSchema,
    current_admin: User = Security(get_current_admin),
    room_service: RoomService = Depends(get_room_service),
):
    return await room_service.update_room(room_id, data)


@router.delete("/room/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    room_id: int,
    current_admin: User = Security(get_current_admin),
    room_service: RoomService = Depends(get_room_service),
):
    await room_service.delete_room(room_id)


# ---------------------------------- BOOKINGS ---------------------------------


@router.get("/bookings/{booking_id}", response_model=BookingResponseSchema)
async def get_booking_by_id(
    booking_id: UUID,
    current_admin: User = Security(get_current_admin),
    booking_service: BookingService = Depends(get_booking_service),
) -> BookingResponseSchema:
    return await booking_service.admin_get_booking_by_id(booking_id)


@router.get("/bookings/", response_model=list[BookingResponseSchema])
async def get_bookings(
    filters: BookingAdminFilterSchema = Depends(),
    skip: int = 0,
    limit: int = 10,
    current_admin: User = Security(get_current_admin),
    booking_service: BookingService = Depends(get_booking_service),
) -> list[BookingResponseSchema]:
    return await booking_service.admin_get_all_bookings(filters, skip, limit)


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


#  ---------------------------------- PAYMENTS ---------------------------------


@router.get("/payments/{payment_id}", response_model=PaymentResponseSchema)
async def get_payment(
    payment_id: UUID,
    current_admin: User = Security(get_current_admin),
    payment_service: PaymentsService = Depends(get_payment_service),
) -> PaymentResponseSchema:
    return await payment_service.get_payment_by_id(payment_id)


@router.get("/payments/", response_model=list[PaymentResponseSchema])
async def list_payments(
    skip: int = 0,
    limit: int = 10,
    current_admin: User = Security(get_current_admin),
    payment_service: PaymentsService = Depends(get_payment_service),
) -> list[PaymentResponseSchema]:
    return await payment_service.admin_get_all_payments(skip=skip, limit=limit)


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
