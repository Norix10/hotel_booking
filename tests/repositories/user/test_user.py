import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from app.models.user import User
from app.repositories.user import UserRepository
from app.models.enums.user_enum import UserRoleEnum
from app.utils.security import get_password_hash


@pytest.mark.asyncio
async def test_empty_users(prepare_db, session: AsyncSession):
    repo = UserRepository(session)
    users = await repo.get_all_users(skip=0, limit=100)
    assert len(users) == 0


@pytest.mark.asyncio
async def test_create_user(prepare_db, session: AsyncSession, user_object: User):
    repo = UserRepository(session)
    user = await repo.create(user_object)
    assert user.id == user_object.id
    assert user.email == user_object.email
    assert user.name == user_object.name


@pytest.mark.asyncio
async def test_get_all_users(prepare_db, session: AsyncSession, create_user: User):
    repo = UserRepository(session)
    users = await repo.get_all_users(skip=0, limit=100)
    assert len(users) == 1
    assert users[0].id == create_user.id


@pytest.mark.asyncio
async def test_get_user_by_id(prepare_db, session: AsyncSession, create_user: User):
    repo = UserRepository(session)
    retrieved_user = await repo.get_by_id(create_user.id)
    assert retrieved_user.id == create_user.id
    assert retrieved_user.email == create_user.email


@pytest.mark.asyncio
async def test_get_user_by_email(prepare_db, session: AsyncSession, create_user: User):
    repo = UserRepository(session)
    retrieved_user = await repo.get_by_email(create_user.email)
    assert retrieved_user.id == create_user.id
    assert retrieved_user.name == create_user.name


@pytest.mark.asyncio
async def test_update_user(
    prepare_db, session: AsyncSession, create_user: User, update_user_payload
):
    repo = UserRepository(session)
    create_user.name = update_user_payload["new_name"]
    hashed_password = get_password_hash(update_user_payload["new_password"])
    create_user.hashed_password = hashed_password
    updated_user = await repo.update(create_user)
    assert updated_user.name == update_user_payload["new_name"]
    assert updated_user.hashed_password == hashed_password


@pytest.mark.asyncio
async def test_delete_user(prepare_db, session: AsyncSession, create_user: User):
    repo = UserRepository(session)
    await repo.delete(create_user)
    deleted_user = await repo.get_by_id(create_user.id)
    assert deleted_user is None


@pytest.mark.asyncio
async def test_get_nonexistent_user(prepare_db, session: AsyncSession):
    repo = UserRepository(session)
    fake_id = uuid4()
    user = await repo.get_by_id(fake_id)
    assert user is None


@pytest.mark.asyncio
async def test_get_user_by_nonexistent_email(prepare_db, session: AsyncSession):
    repo = UserRepository(session)
    user = await repo.get_by_email("nonexistent@example.com")
    assert user is None
