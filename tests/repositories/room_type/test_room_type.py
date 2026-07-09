import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.room_type import RoomTypeRepository
from app.models.room_type import RoomType
from app.models.enums.room_enum import RoomBedTypeEnum
from app.schemas.room_type import RoomTypeFilterSchema


@pytest.mark.asyncio
async def test_create_room_type(prepare_db, session: AsyncSession, room_type_payload):
    repo = RoomTypeRepository(session)
    room_type = RoomType(**room_type_payload)
    created = await repo.create(room_type)
    assert created.id is not None
    assert created.name == room_type_payload["name"]


@pytest.mark.asyncio
async def test_get_by_id(prepare_db, session: AsyncSession, create_room_type):
    repo = RoomTypeRepository(session)
    room_type = await repo.get_by_id(create_room_type.id)
    assert room_type.id == create_room_type.id


@pytest.mark.asyncio
async def test_get_by_id_not_found(prepare_db, session: AsyncSession):
    repo = RoomTypeRepository(session)
    room_type = await repo.get_by_id(999999)
    assert room_type is None


@pytest.mark.asyncio
async def test_get_room_types(prepare_db, session: AsyncSession, create_room_type):
    repo = RoomTypeRepository(session)
    room_types = await repo.get_room_types()
    assert len(room_types) == 1


@pytest.mark.asyncio
async def test_get_room_types_with_filters(
    prepare_db, session: AsyncSession, create_room_type
):
    repo = RoomTypeRepository(session)
    matching = RoomTypeFilterSchema(bed_type=RoomBedTypeEnum.double)
    room_types = await repo.get_room_types(filters=matching)
    assert len(room_types) == 1

    non_matching = RoomTypeFilterSchema(bed_type=RoomBedTypeEnum.king)
    empty = await repo.get_room_types(filters=non_matching)
    assert len(empty) == 0


@pytest.mark.asyncio
async def test_update_room_type(prepare_db, session: AsyncSession, create_room_type):
    repo = RoomTypeRepository(session)
    create_room_type.base_price = 200
    updated = await repo.update(create_room_type)
    assert updated.base_price == 200


@pytest.mark.asyncio
async def test_delete_room_type(prepare_db, session: AsyncSession, create_room_type):
    repo = RoomTypeRepository(session)
    await repo.delete(create_room_type)
    deleted = await repo.get_by_id(create_room_type.id)
    assert deleted is None


@pytest.mark.asyncio
async def test_delete_all_room_types(
    prepare_db, session: AsyncSession, create_room_type
):
    repo = RoomTypeRepository(session)
    await repo.delete_all()
    room_types = await repo.get_room_types()
    assert len(room_types) == 0
