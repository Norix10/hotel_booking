import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.services.room import RoomService
from app.repositories.room import RoomRepository
from app.schemas.room import RoomCreateSchema, RoomUpdateSchema
from app.models.enums.room_enum import RoomStatusTypeEnum


def build_service(session: AsyncSession) -> RoomService:
    return RoomService(RoomRepository(session))


@pytest.mark.asyncio
async def test_create_room(
    prepare_db, session: AsyncSession, create_room_type, room_payload
):
    service = build_service(session)
    data = RoomCreateSchema(room_type_id=create_room_type.id, **room_payload)
    room = await service.create_room(data)
    assert room.room_name == room_payload["room_name"]


@pytest.mark.asyncio
async def test_get_all_rooms(prepare_db, session: AsyncSession, create_room):
    service = build_service(session)
    rooms = await service.get_all_rooms()
    assert len(rooms) == 1


@pytest.mark.asyncio
async def test_get_availible_rooms(prepare_db, session: AsyncSession, create_room):
    service = build_service(session)
    rooms = await service.get_availible_rooms()
    assert len(rooms) == 1


@pytest.mark.asyncio
async def test_update_room(prepare_db, session: AsyncSession, create_room):
    service = build_service(session)
    data = RoomUpdateSchema(status=RoomStatusTypeEnum.cleaning)
    updated = await service.update_room(create_room.id, data)
    assert updated.status == RoomStatusTypeEnum.cleaning


@pytest.mark.asyncio
async def test_update_room_not_found(prepare_db, session: AsyncSession):
    service = build_service(session)
    data = RoomUpdateSchema(status=RoomStatusTypeEnum.cleaning)
    with pytest.raises(HTTPException) as exc_info:
        await service.update_room(999999, data)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_room(prepare_db, session: AsyncSession, create_room):
    service = build_service(session)
    await service.delete_room(create_room.id)
    with pytest.raises(HTTPException):
        await service._get_room_or_404(create_room.id)


@pytest.mark.asyncio
async def test_delete_room_not_found(prepare_db, session: AsyncSession):
    service = build_service(session)
    with pytest.raises(HTTPException) as exc_info:
        await service.delete_room(999999)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
