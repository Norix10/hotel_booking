import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.room import RoomRepository
from app.models.room import Room
from app.models.enums.room_enum import RoomStatusTypeEnum


@pytest.mark.asyncio
async def test_create_room(
    prepare_db, session: AsyncSession, create_room_type, room_payload
):
    repo = RoomRepository(session)
    room = Room(room_type_id=create_room_type.id, **room_payload)
    created = await repo.create(room)
    assert created.id is not None
    assert created.room_name == room_payload["room_name"]


@pytest.mark.asyncio
async def test_get_by_id(prepare_db, session: AsyncSession, create_room):
    repo = RoomRepository(session)
    room = await repo.get_by_id(create_room.id)
    assert room.id == create_room.id


@pytest.mark.asyncio
async def test_get_by_id_not_found(prepare_db, session: AsyncSession):
    repo = RoomRepository(session)
    room = await repo.get_by_id(999999)
    assert room is None


@pytest.mark.asyncio
async def test_get_available_rooms(prepare_db, session: AsyncSession, create_room):
    repo = RoomRepository(session)
    rooms = await repo.get_availble_rooms()
    assert len(rooms) == 1


@pytest.mark.asyncio
async def test_get_available_rooms_excludes_occupied(
    prepare_db, session: AsyncSession, create_room
):
    create_room.status = RoomStatusTypeEnum.occupied
    await session.commit()
    repo = RoomRepository(session)
    rooms = await repo.get_availble_rooms()
    assert len(rooms) == 0


@pytest.mark.asyncio
async def test_get_with_type(prepare_db, session: AsyncSession, create_room):
    repo = RoomRepository(session)
    room = await repo.get_with_type(create_room.id)
    assert room.id == create_room.id
    assert room.room_types is not None


@pytest.mark.asyncio
async def test_update_room(prepare_db, session: AsyncSession, create_room):
    repo = RoomRepository(session)
    create_room.floor = 5
    updated = await repo.update(create_room)
    assert updated.floor == 5


@pytest.mark.asyncio
async def test_delete_room(prepare_db, session: AsyncSession, create_room):
    repo = RoomRepository(session)
    await repo.delete(create_room)
    deleted = await repo.get_by_id(create_room.id)
    assert deleted is None
