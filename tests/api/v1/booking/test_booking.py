from http import HTTPStatus
from datetime import timedelta
from uuid import uuid4
import pytest
from httpx import AsyncClient

from app.models.room import Room


@pytest.mark.asyncio
async def test_create_booking(
    prepare_db,
    create_user,
    create_room: Room,
    booking_payload,
    access_token: str,
    async_client: AsyncClient,
):
    payload = {
        "room_id": booking_payload["room_id"],
        "check_in": booking_payload["check_in"].isoformat(),
        "check_out": booking_payload["check_out"].isoformat(),
    }
    response = await async_client.post(
        "/api/v1/bookings/",
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.CREATED
    response_json = response.json()
    assert response_json["room_id"] == create_room.id
    assert response_json["status"] == "pending"


@pytest.mark.asyncio
async def test_create_booking_without_token(
    prepare_db, booking_payload, async_client: AsyncClient
):
    payload = {
        "room_id": booking_payload["room_id"],
        "check_in": booking_payload["check_in"].isoformat(),
        "check_out": booking_payload["check_out"].isoformat(),
    }
    response = await async_client.post("/api/v1/bookings/", json=payload)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_my_bookings(
    prepare_db, create_booking, access_token: str, async_client: AsyncClient
):
    response = await async_client.get(
        "/api/v1/bookings/", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_booking_by_id(
    prepare_db, create_booking, access_token: str, async_client: AsyncClient
):
    response = await async_client.get(
        f"/api/v1/bookings/{create_booking.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == str(create_booking.id)


@pytest.mark.asyncio
async def test_get_booking_by_id_not_found(
    prepare_db, access_token: str, async_client: AsyncClient
):
    response = await async_client.get(
        f"/api/v1/bookings/{uuid4()}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_update_booking(
    prepare_db, create_booking, access_token: str, async_client: AsyncClient
):
    new_check_in = create_booking.check_out.date() + timedelta(days=5)
    new_check_out = new_check_in + timedelta(days=2)
    response = await async_client.patch(
        f"/api/v1/bookings/{create_booking.id}",
        json={
            "check_in": new_check_in.isoformat(),
            "check_out": new_check_out.isoformat(),
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_cancel_booking(
    prepare_db, create_booking, access_token: str, async_client: AsyncClient
):
    response = await async_client.patch(
        f"/api/v1/bookings/{create_booking.id}/cancel",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["status"] == "cancelled"