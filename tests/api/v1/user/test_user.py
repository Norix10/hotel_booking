from http import HTTPStatus

import pytest
from httpx import AsyncClient

from app.models.user import User


@pytest.mark.asyncio
async def test_register_user(prepare_db, user_payload, async_client: AsyncClient):
    response = await async_client.post("/api/v1/user", json=user_payload)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json["name"] == user_payload["name"]
    assert response_json["email"] == user_payload["email"]


@pytest.mark.asyncio
async def test_register_user_with_duplicate_email(
    prepare_db, create_user: User, user_payload, async_client: AsyncClient
):
    response = await async_client.post("/api/v1/user", json=user_payload)
    assert response.status_code == HTTPStatus.CONFLICT


@pytest.mark.asyncio
async def test_register_user_with_invalid_email(prepare_db, async_client: AsyncClient):
    payload = {
        "name": "Test User",
        "email": "invalid-email",
        "password": "Password123!",
    }
    response = await async_client.post("/api/v1/user", json=payload)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_signin_user(
    prepare_db, create_user: User, user_payload, async_client: AsyncClient
):
    signin_payload = {
        "email": user_payload["email"],
        "password": user_payload["password"],
    }
    response = await async_client.post("/api/v1/user/signin", json=signin_payload)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert "access_token" in response_json
    assert response_json["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_signin_user_with_invalid_email(prepare_db, async_client: AsyncClient):
    signin_payload = {
        "email": "nonexistent@example.com",
        "password": "SomePassword123!",
    }
    response = await async_client.post("/api/v1/user/signin", json=signin_payload)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_signin_user_with_wrong_password(
    prepare_db, create_user: User, user_payload, async_client: AsyncClient
):
    signin_payload = {"email": user_payload["email"], "password": "WrongPassword123!"}
    response = await async_client.post("/api/v1/user/signin", json=signin_payload)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_get_me(
    prepare_db, create_user: User, access_token: str, async_client: AsyncClient
):
    response = await async_client.get(
        "/api/v1/user/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json["id"] == str(create_user.id)
    assert response_json["email"] == create_user.email
    assert response_json["name"] == create_user.name


@pytest.mark.asyncio
async def test_get_me_without_token(prepare_db, async_client: AsyncClient):
    response = await async_client.get("/api/v1/user/me")
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_update_me(
    prepare_db,
    create_user: User,
    access_token: str,
    async_client: AsyncClient,
    update_user_payload,
):
    response = await async_client.patch(
        "/api/v1/user/",
        json={"name": update_user_payload["new_name"]},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json["id"] == str(create_user.id)
    assert response_json["name"] == update_user_payload["new_name"]


@pytest.mark.asyncio
async def test_delete_me(
    prepare_db, create_user: User, access_token: str, async_client: AsyncClient
):
    response = await async_client.delete(
        "/api/v1/user/", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
