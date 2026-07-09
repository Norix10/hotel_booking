from http import HTTPStatus
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_users_list(
    prepare_db,
    create_admin,
    create_user,
    admin_access_token: str,
    async_client: AsyncClient,
):
    response = await async_client.get(
        "/api/v1/admin/users/",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    emails = {user["email"] for user in response.json()}
    assert create_user.email in emails


@pytest.mark.asyncio
async def test_get_users_list_forbidden_for_regular_user(
    prepare_db, create_user, access_token: str, async_client: AsyncClient
):
    response = await async_client.get(
        "/api/v1/admin/users/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio
async def test_delete_user_by_id(
    prepare_db,
    create_admin,
    create_user,
    admin_access_token: str,
    async_client: AsyncClient,
):
    response = await async_client.delete(
        f"/api/v1/admin/users/{create_user.id}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_create_room_type(
    prepare_db,
    create_admin,
    room_type_payload,
    admin_access_token: str,
    async_client: AsyncClient,
):
    payload = {
        **room_type_payload,
        "bed_type": room_type_payload["bed_type"].value,
        "bathroom_type": room_type_payload["bathroom_type"].value,
    }
    response = await async_client.post(
        "/api/v1/admin/room-types/",
        json=payload,
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["name"] == room_type_payload["name"]


@pytest.mark.asyncio
async def test_update_room_type(
    prepare_db,
    create_admin,
    create_room_type,
    admin_access_token: str,
    async_client: AsyncClient,
):
    response = await async_client.patch(
        f"/api/v1/admin/room-types/{create_room_type.id}",
        json={"base_price": 500},
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["base_price"] == 500


@pytest.mark.asyncio
async def test_delete_room_type(
    prepare_db,
    create_admin,
    create_room_type,
    admin_access_token: str,
    async_client: AsyncClient,
):
    response = await async_client.delete(
        f"/api/v1/admin/room-types/{create_room_type.id}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_create_room(
    prepare_db,
    create_admin,
    create_room_type,
    room_payload,
    admin_access_token: str,
    async_client: AsyncClient,
):
    payload = {
        **room_payload,
        "room_type_id": create_room_type.id,
        "status": room_payload["status"].value,
    }
    response = await async_client.post(
        "/api/v1/admin/room/",
        json=payload,
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["room_name"] == room_payload["room_name"]


@pytest.mark.asyncio
async def test_update_room(
    prepare_db,
    create_admin,
    create_room,
    admin_access_token: str,
    async_client: AsyncClient,
):
    response = await async_client.patch(
        f"/api/v1/admin/room/{create_room.id}",
        json={"floor": 9},
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["floor"] == 9


@pytest.mark.asyncio
async def test_delete_room(
    prepare_db,
    create_admin,
    create_room,
    admin_access_token: str,
    async_client: AsyncClient,
):
    response = await async_client.delete(
        f"/api/v1/admin/room/{create_room.id}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_admin_get_booking_by_id(
    prepare_db,
    create_admin,
    create_booking,
    admin_access_token: str,
    async_client: AsyncClient,
):
    response = await async_client.get(
        f"/api/v1/admin/bookings/{create_booking.id}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == str(create_booking.id)


@pytest.mark.asyncio
async def test_admin_get_bookings_list(
    prepare_db,
    create_admin,
    create_booking,
    admin_access_token: str,
    async_client: AsyncClient,
):
    response = await async_client.get(
        "/api/v1/admin/bookings/",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_admin_update_booking(
    prepare_db,
    create_admin,
    create_booking,
    admin_access_token: str,
    async_client: AsyncClient,
):
    response = await async_client.patch(
        f"/api/v1/admin/bookings/{create_booking.id}",
        json={"status": "confirmed"},
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["status"] == "confirmed"


@pytest.mark.asyncio
async def test_admin_delete_booking(
    prepare_db,
    create_admin,
    create_booking,
    admin_access_token: str,
    async_client: AsyncClient,
):
    response = await async_client.delete(
        f"/api/v1/admin/bookings/{create_booking.id}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_admin_get_payment(
    prepare_db,
    create_admin,
    create_payment,
    admin_access_token: str,
    async_client: AsyncClient,
):
    response = await async_client.get(
        f"/api/v1/admin/payments/{create_payment.id}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == str(create_payment.id)


@pytest.mark.asyncio
async def test_admin_list_payments(
    prepare_db,
    create_admin,
    create_payment,
    admin_access_token: str,
    async_client: AsyncClient,
):
    response = await async_client.get(
        "/api/v1/admin/payments/",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_admin_update_payment(
    prepare_db,
    create_admin,
    create_payment,
    admin_access_token: str,
    async_client: AsyncClient,
):
    response = await async_client.patch(
        f"/api/v1/admin/payments/{create_payment.id}",
        json={"payment_status": "refunded"},
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["payment_status"] == "refunded"


@pytest.mark.asyncio
async def test_admin_delete_payment(
    prepare_db,
    create_admin,
    create_payment,
    admin_access_token: str,
    async_client: AsyncClient,
):
    response = await async_client.delete(
        f"/api/v1/admin/payments/{create_payment.id}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
