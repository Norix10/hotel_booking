import pytest
import pytest_asyncio
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.room_type import RoomType
from app.models.room import Room
from app.models.booking import Booking
from app.models.enums.room_enum import (
    RoomBedTypeEnum,
    RoomBathroomTypeEnum,
    RoomStatusTypeEnum,
)
from app.models.enums.booking_enum import BookingStatusEnum


@pytest.fixture()
def room_type_payload():
    return {
        "name": "Standard Room",
        "base_price": 100,
        "capacity": 2,
        "bed_type": RoomBedTypeEnum.double,
        "bathroom_type": RoomBathroomTypeEnum.shower,
        "area_sq_m": 25,
        "has_ac": True,
        "has_wifi": True,
    }


@pytest.fixture()
def room_type_object(room_type_payload) -> RoomType:
    return RoomType(**room_type_payload)


@pytest_asyncio.fixture(scope="function")
async def create_room_type(
    session: AsyncSession, room_type_object: RoomType
) -> RoomType:
    session.add(room_type_object)
    await session.commit()
    await session.refresh(room_type_object)
    return room_type_object


@pytest.fixture()
def room_payload():
    return {
        "room_name": "101",
        "floor": 1,
        "status": RoomStatusTypeEnum.available,
    }


@pytest_asyncio.fixture(scope="function")
async def create_room(
    prepare_db, session: AsyncSession, create_room_type: RoomType, room_payload
) -> Room:
    room = Room(room_type_id=create_room_type.id, **room_payload)
    session.add(room)
    await session.commit()
    await session.refresh(room)
    return room


@pytest.fixture()
def booking_payload(create_room):
    check_in = datetime.now(timezone.utc) + timedelta(days=1)
    check_out = check_in + timedelta(days=3)
    return {
        "room_id": create_room.id,
        "check_in": check_in,
        "check_out": check_out,
    }


@pytest_asyncio.fixture(scope="function")
async def create_booking(
    prepare_db, session: AsyncSession, create_user, booking_payload
) -> Booking:
    booking = Booking(
        user_id=create_user.id,
        room_id=booking_payload["room_id"],
        check_in=booking_payload["check_in"],
        check_out=booking_payload["check_out"],
        status=BookingStatusEnum.pending,
    )
    session.add(booking)
    await session.commit()
    await session.refresh(booking)
    return booking


@pytest.fixture()
def update_booking_payload():
    check_in = datetime.now(timezone.utc) + timedelta(days=10)
    check_out = check_in + timedelta(days=2)
    return {"check_in": check_in, "check_out": check_out}