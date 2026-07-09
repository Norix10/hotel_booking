from http import HTTPStatus
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_all_room_types(
    prepare_db, create_room_type, async_client: AsyncClient
):
    response = await async_client.get("/api/v1/room-types/")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_room_type_by_id(
    prepare_db, create_room_type, async_client: AsyncClient
):
    response = await async_client.get(f"/api/v1/room-types/{create_room_type.id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == create_room_type.id


@pytest.mark.asyncio
async def test_get_room_type_by_id_not_found(prepare_db, async_client: AsyncClient):
    response = await async_client.get("/api/v1/room-types/999999")
    assert response.status_code == HTTPStatus.NOT_FOUND
