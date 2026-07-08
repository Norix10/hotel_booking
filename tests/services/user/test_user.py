import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from app.schemas.user import UserCreateSchema, UserUpdateSchema
from app.services.user import UserService
from app.repositories.user import UserRepository
from fastapi import HTTPException, status


@pytest.mark.asyncio
async def test_get_all_users_empty(prepare_db, session: AsyncSession):
    repo = UserRepository(session)
    service = UserService(repo)
    users = await service.get_all_users()
    assert len(users) == 0


@pytest.mark.asyncio
async def test_create_user(prepare_db, session: AsyncSession, user_payload):
    repo = UserRepository(session)
    service = UserService(repo)
    data = UserCreateSchema(
        name=user_payload["name"],
        email=user_payload["email"],
        password=user_payload["password"],
    )
    user = await service.create_user(data)
    assert user.name == user_payload["name"]
    assert user.email == user_payload["email"]


@pytest.mark.asyncio
async def test_get_user_by_id(prepare_db, session: AsyncSession, create_user):
    repo = UserRepository(session)
    service = UserService(repo)
    user = await service.get_user_by_id(create_user.id)
    assert user.id == create_user.id
    assert user.email == create_user.email


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(prepare_db, session: AsyncSession):
    repo = UserRepository(session)
    service = UserService(repo)
    with pytest.raises(HTTPException) as exc_info:
        await service.get_user_by_id(uuid4())
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_user_by_email(prepare_db, session: AsyncSession, create_user):
    repo = UserRepository(session)
    service = UserService(repo)
    user = await service.get_user_by_email(create_user.email)
    assert user.id == create_user.id
    assert user.name == create_user.name


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(prepare_db, session: AsyncSession):
    repo = UserRepository(session)
    service = UserService(repo)
    with pytest.raises(HTTPException) as exc_info:
        await service.get_user_by_email("nonexistent@example.com")
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_user_with_duplicate_email(
    prepare_db, session: AsyncSession, create_user, user_payload
):
    repo = UserRepository(session)
    service = UserService(repo)
    data = UserCreateSchema(
        name="Another User",
        email=create_user.email,
        password="AnotherPassword123!",
    )
    with pytest.raises(HTTPException) as exc_info:
        await service.create_user(data)
    assert exc_info.value.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_update_user(
    prepare_db, session: AsyncSession, create_user, update_user_payload
):
    repo = UserRepository(session)
    service = UserService(repo)
    data = UserUpdateSchema(name=update_user_payload["new_name"])
    updated_user = await service.update_user(create_user.id, data)
    assert updated_user.name == update_user_payload["new_name"]


@pytest.mark.asyncio
async def test_update_nonexistent_user(prepare_db, session: AsyncSession):
    repo = UserRepository(session)
    service = UserService(repo)
    data = UserUpdateSchema(name="New Name")
    with pytest.raises(HTTPException) as exc_info:
        await service.update_user(uuid4(), data)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_user(prepare_db, session: AsyncSession, create_user):
    repo = UserRepository(session)
    service = UserService(repo)
    await service.delete_user(create_user.id)
    with pytest.raises(HTTPException):
        await service.get_user_by_id(create_user.id)


@pytest.mark.asyncio
async def test_delete_nonexistent_user(prepare_db, session: AsyncSession):
    repo = UserRepository(session)
    service = UserService(repo)
    with pytest.raises(HTTPException) as exc_info:
        await service.delete_user(uuid4())
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
