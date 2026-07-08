import pytest
from uuid import uuid4
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.booking import BookingRepository
from app.models.booking import Booking
from app.models.enums.booking_enum import BookingStatusEnum
from app.schemas.booking import BookingAdminFilterSchema


@pytest.mark.asyncio
async def test_create_booking(
    prepare_db, session: AsyncSession, create_user, create_room, booking_payload
):
    repo = BookingRepository(session)
    booking = Booking(
        user_id=create_user.id,
        room_id=booking_payload["room_id"],
        check_in=booking_payload["check_in"],
        check_out=booking_payload["check_out"],
        status=BookingStatusEnum.pending,
    )
    created = await repo.create(booking)
    assert created.id is not None
    assert created.room_id == create_room.id


@pytest.mark.asyncio
async def test_get_by_id(prepare_db, session: AsyncSession, create_booking):
    repo = BookingRepository(session)
    booking = await repo.get_by_id(create_booking.id)
    assert booking.id == create_booking.id


@pytest.mark.asyncio
async def test_get_by_id_not_found(prepare_db, session: AsyncSession):
    repo = BookingRepository(session)
    booking = await repo.get_by_id(uuid4())
    assert booking is None


@pytest.mark.asyncio
async def test_get_user_booking_by_booking_id(
    prepare_db, session: AsyncSession, create_user, create_booking
):
    repo = BookingRepository(session)
    booking = await repo.get_user_booking_by_booking_id(
        create_user.id, create_booking.id
    )
    assert booking.id == create_booking.id


@pytest.mark.asyncio
async def test_get_by_user_id(
    prepare_db, session: AsyncSession, create_user, create_booking
):
    repo = BookingRepository(session)
    bookings = await repo.get_by_user_id(create_user.id)
    assert len(bookings) == 1
    assert bookings[0].id == create_booking.id


@pytest.mark.asyncio
async def test_get_by_user_id_with_status_filter(
    prepare_db, session: AsyncSession, create_user, create_booking
):
    repo = BookingRepository(session)
    pending = await repo.get_by_user_id(create_user.id, status=BookingStatusEnum.pending)
    assert len(pending) == 1
    confirmed = await repo.get_by_user_id(
        create_user.id, status=BookingStatusEnum.confirmed
    )
    assert len(confirmed) == 0


@pytest.mark.asyncio
async def test_check_room_overlap_true(
    prepare_db, session: AsyncSession, create_room, create_booking
):
    repo = BookingRepository(session)
    overlap = await repo.check_room_overlap(
        create_room.id, create_booking.check_in, create_booking.check_out
    )
    assert overlap is True


@pytest.mark.asyncio
async def test_check_room_overlap_false(
    prepare_db, session: AsyncSession, create_room, create_booking
):
    repo = BookingRepository(session)
    far_check_in = create_booking.check_out + timedelta(days=10)
    far_check_out = far_check_in + timedelta(days=2)
    overlap = await repo.check_room_overlap(create_room.id, far_check_in, far_check_out)
    assert overlap is False


@pytest.mark.asyncio
async def test_check_room_overlap_excludes_booking(
    prepare_db, session: AsyncSession, create_room, create_booking
):
    repo = BookingRepository(session)
    overlap = await repo.check_room_overlap(
        create_room.id,
        create_booking.check_in,
        create_booking.check_out,
        exclude_booking_id=create_booking.id,
    )
    assert overlap is False


@pytest.mark.asyncio
async def test_get_by_room_id(
    prepare_db, session: AsyncSession, create_room, create_booking
):
    repo = BookingRepository(session)
    bookings = await repo.get_by_room_id(create_room.id)
    assert len(bookings) == 1


@pytest.mark.asyncio
async def test_get_active_bookings(prepare_db, session: AsyncSession, create_booking):
    repo = BookingRepository(session)
    bookings = await repo.get_active_bookings()
    assert len(bookings) == 1


@pytest.mark.asyncio
async def test_get_all_bookings(prepare_db, session: AsyncSession, create_booking):
    repo = BookingRepository(session)
    filters = BookingAdminFilterSchema()
    bookings = await repo.get_all_bookings(filters=filters)
    assert len(bookings) == 1


@pytest.mark.asyncio
async def test_update_booking(prepare_db, session: AsyncSession, create_booking):
    repo = BookingRepository(session)
    create_booking.status = BookingStatusEnum.confirmed
    updated = await repo.update(create_booking)
    assert updated.status == BookingStatusEnum.confirmed


@pytest.mark.asyncio
async def test_delete_booking(prepare_db, session: AsyncSession, create_booking):
    repo = BookingRepository(session)
    await repo.delete(create_booking)
    deleted = await repo.get_by_id(create_booking.id)
    assert deleted is None