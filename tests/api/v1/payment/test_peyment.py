from http import HTTPStatus
import pytest
from httpx import AsyncClient

from app.models.payment import Payment


@pytest.mark.asyncio
async def test_create_payment(
    prepare_db,
    create_booking,
    access_token: str,
    async_client: AsyncClient,
    monkeypatch,
):
    monkeypatch.setattr(
        "app.tasks.payment_tasks.process_payment_bg.delay", lambda *a, **kw: None
    )
    response = await async_client.post(
        f"/api/v1/payments/{create_booking.id}",
        json={"payment_method": "card"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.CREATED
    response_json = response.json()
    assert response_json["booking_id"] == str(create_booking.id)


@pytest.mark.asyncio
async def test_create_payment_without_token(
    prepare_db, create_booking, async_client: AsyncClient
):
    response = await async_client.post(
        f"/api/v1/payments/{create_booking.id}",
        json={"payment_method": "card"},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_my_payments(
    prepare_db, create_payment: Payment, access_token: str, async_client: AsyncClient
):
    response = await async_client.get(
        "/api/v1/payments/", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1
