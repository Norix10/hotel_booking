import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.services.room_type import RoomTypesService
from app.repositories.room_type import RoomTypeRepository
from app.schemas.room_type import RoomTypeCreateSchema, RoomTypeUpdateSchema


def build_service(session: AsyncSession) -> RoomTypesService:
    return RoomTypesService(RoomTypeRepository(session))


@pytest.mark.asyncio
async def test_create_room_type(prepare_db, session: AsyncSession, room_type_payload):
    service = build_service(session)
    data = RoomTypeCreateSchema(**room_type_payload)
    room_type = await service.create_room_type(data)
    assert room_type.name == room_type_payload["name"]
    assert room_type.base_price == room_type_payload["base_price"]


@pytest.mark.asyncio
async def test_get_all_room_types(prepare_db, session: AsyncSession, create_room_type):
    service = build_service(session)
    room_types = await service.get_all_room_types()
    assert len(room_types) == 1


@pytest.mark.asyncio
async def test_update_room_type(prepare_db, session: AsyncSession, create_room_type):
    service = build_service(session)
    data = RoomTypeUpdateSchema(base_price=250)
    updated = await service.update_room_type(create_room_type.id, data)
    assert updated.base_price == 250


@pytest.mark.asyncio
async def test_update_room_type_not_found(prepare_db, session: AsyncSession):
    service = build_service(session)
    data = RoomTypeUpdateSchema(base_price=250)
    with pytest.raises(HTTPException) as exc_info:
        await service.update_room_type(999999, data)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_room_type(prepare_db, session: AsyncSession, create_room_type):
    service = build_service(session)
    await service.delete_room_type(create_room_type.id)
    with pytest.raises(HTTPException):
        await service._get_room_type_or_404(create_room_type.id)


@pytest.mark.asyncio
async def test_delete_room_type_not_found(prepare_db, session: AsyncSession):
    service = build_service(session)
    with pytest.raises(HTTPException) as exc_info:
        await service.delete_room_type(999999)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_all_room_types(
    prepare_db, session: AsyncSession, create_room_type
):
    service = build_service(session)
    await service.delete_all_room_types()
    room_types = await service.get_all_room_types()
    assert len(room_types) == 0
