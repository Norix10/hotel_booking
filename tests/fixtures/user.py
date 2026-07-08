import pytest
import pytest_asyncio
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_user_service
from app.models.user import User
from app.schemas.auth import AccessTokenDataSchema
from app.services.auth import create_access_token
from app.utils.security import get_password_hash


@pytest.fixture()
def user_payload():
    return {
        "name": "User Userson",
        "email": "tuser.userson@example.com",
        "password": "!67Password",
    }


@pytest.fixture()
def user_object(user_payload) -> User:
    return User(
        id=UUID("fa534625-9b5c-4609-88aa-d4ad1c9aec56"),
        name=user_payload["name"],
        email=user_payload["email"],
        hashed_password=get_password_hash(user_payload["password"]),
    )


@pytest_asyncio.fixture(scope="function")
async def create_user(session: AsyncSession, user_object: User) -> User:
    session.add(user_object)
    await session.commit()
    return user_object


@pytest.fixture()
def access_token(user_payload):
    token_data = AccessTokenDataSchema(sub=user_payload["email"])
    return create_access_token(token_data)


@pytest.fixture()
def update_user_payload():
    return {"new_name": "User Second", "new_password": "Password67!"}
