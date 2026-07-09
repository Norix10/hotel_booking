from http import HTTPStatus
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_all_rooms(prepare_db, create_room, async_client: AsyncClient):
    response = await async_client.get("/api/v1/room/")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_available_rooms(prepare_db, create_room, async_client: AsyncClient):
    response = await async_client.get("/api/v1/room/available")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_room_by_id(prepare_db, create_room, async_client: AsyncClient):
    response = await async_client.get(f"/api/v1/room/{create_room.id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == create_room.id


@pytest.mark.asyncio
async def test_get_room_by_id_not_found(prepare_db, async_client: AsyncClient):
    response = await async_client.get("/api/v1/room/999999")
    assert response.status_code == HTTPStatus.NOT_FOUND
