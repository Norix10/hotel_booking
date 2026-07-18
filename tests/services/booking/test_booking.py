import pytest
from uuid import uuid4
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.services.booking import BookingService
from app.repositories.booking import BookingRepository
from app.repositories.room import RoomRepository
from app.repositories.payment import PaymentRepository
from app.schemas.booking import (
    BookingCreateSchema,
    BookingUpdateSchema,
    BookingAdminUpdateSchema,
)
from app.models.enums.booking_enum import BookingStatusEnum
from app.models.enums.room_enum import RoomStatusTypeEnum


def build_service(session: AsyncSession) -> BookingService:
    return BookingService(
        BookingRepository(session),
        RoomRepository(session),
        PaymentRepository(session),
    )


@pytest.mark.asyncio
async def test_create_booking(
    prepare_db, session: AsyncSession, create_user, create_room, booking_payload
):
    service = build_service(session)
    data = BookingCreateSchema(
        room_id=booking_payload["room_id"],
        check_in=booking_payload["check_in"],
        check_out=booking_payload["check_out"],
    )
    booking = await service.create_booking(create_user.id, data)
    assert booking.room_id == create_room.id
    assert booking.status == BookingStatusEnum.pending


@pytest.mark.asyncio
async def test_create_booking_room_not_found(
    prepare_db, session: AsyncSession, create_user, booking_payload
):
    service = build_service(session)
    data = BookingCreateSchema(
        room_id=999999,
        check_in=booking_payload["check_in"],
        check_out=booking_payload["check_out"],
    )
    with pytest.raises(HTTPException) as exc_info:
        await service.create_booking(create_user.id, data)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_booking_ignores_room_operational_status(
    prepare_db, session: AsyncSession, create_user, create_room, booking_payload
):
    create_room.status = RoomStatusTypeEnum.occupied
    await session.commit()
    service = build_service(session)
    data = BookingCreateSchema(
        room_id=booking_payload["room_id"],
        check_in=booking_payload["check_in"],
        check_out=booking_payload["check_out"],
    )
    booking = await service.create_booking(create_user.id, data)
    assert booking.status == BookingStatusEnum.pending


@pytest.mark.asyncio
async def test_create_booking_overlapping_dates(
    prepare_db, session: AsyncSession, create_user, create_booking
):
    service = build_service(session)
    data = BookingCreateSchema(
        room_id=create_booking.room_id,
        check_in=create_booking.check_in.date(),
        check_out=create_booking.check_out.date(),
    )
    with pytest.raises(HTTPException) as exc_info:
        await service.create_booking(create_user.id, data)
    assert exc_info.value.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_get_user_booking_by_id(
    prepare_db, session: AsyncSession, create_user, create_booking
):
    service = build_service(session)
    booking = await service.get_user_booking_by_id(create_user.id, create_booking.id)
    assert booking.id == create_booking.id


@pytest.mark.asyncio
async def test_get_user_booking_by_id_not_found(
    prepare_db, session: AsyncSession, create_user
):
    service = build_service(session)
    with pytest.raises(HTTPException) as exc_info:
        await service.get_user_booking_by_id(create_user.id, uuid4())
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_all_user_bookings(
    prepare_db, session: AsyncSession, create_user, create_booking
):
    service = build_service(session)
    bookings = await service.get_all_user_bookings(create_user.id)
    assert len(bookings) == 1


@pytest.mark.asyncio
async def test_update_booking(
    prepare_db, session: AsyncSession, create_user, create_booking
):
    service = build_service(session)
    new_check_in = create_booking.check_out.date() + timedelta(days=5)
    new_check_out = new_check_in + timedelta(days=2)
    data = BookingUpdateSchema(check_in=new_check_in, check_out=new_check_out)
    updated = await service.update_booking(create_user.id, create_booking.id, data)
    assert updated.check_in.date() == new_check_in


@pytest.mark.asyncio
async def test_update_booking_not_found(prepare_db, session: AsyncSession, create_user):
    service = build_service(session)
    data = BookingUpdateSchema()
    with pytest.raises(HTTPException) as exc_info:
        await service.update_booking(create_user.id, uuid4(), data)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_confirm_booking(
    prepare_db, session: AsyncSession, create_user, create_booking
):
    service = build_service(session)
    confirmed = await service.confirm_booking(create_user.id, create_booking.id)
    assert confirmed.status == BookingStatusEnum.confirmed


@pytest.mark.asyncio
async def test_cancel_booking(
    prepare_db, session: AsyncSession, create_user, create_booking
):
    service = build_service(session)
    cancelled = await service.cancel_booking(create_user.id, create_booking.id)
    assert cancelled.status == BookingStatusEnum.cancelled


@pytest.mark.asyncio
async def test_admin_get_booking_by_id(
    prepare_db, session: AsyncSession, create_booking
):
    service = build_service(session)
    booking = await service.admin_get_booking_by_id(create_booking.id)
    assert booking.id == create_booking.id


@pytest.mark.asyncio
async def test_admin_update_booking(prepare_db, session: AsyncSession, create_booking):
    service = build_service(session)
    data = BookingAdminUpdateSchema(status=BookingStatusEnum.confirmed)
    updated = await service.admin_update_booking(create_booking.id, data)
    assert updated.status == BookingStatusEnum.confirmed


@pytest.mark.asyncio
async def test_admin_delete_booking(prepare_db, session: AsyncSession, create_booking):
    service = build_service(session)
    await service.admin_delete_booking(create_booking.id)
    with pytest.raises(HTTPException):
        await service.admin_get_booking_by_id(create_booking.id)