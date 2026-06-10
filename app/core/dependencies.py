import jwt
from jwt import InvalidTokenError
from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.config import settings
from app.db.database import get_db_session
from app.utils.exceptions import NotFoundException, UnauthenticatedException
from app.models.enums.user_enum import UserRole

from app.services.user import UserService

from app.repositories.user import UserRepository

from app.models.user import User

bearer_scheme = HTTPBearer()


async def get_user_repo(
    session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    return UserRepository(session)


async def get_user_service(
    user_repo: UserRepository = Depends(get_user_repo),
) -> UserService:
    return UserService(user_repo)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return payload


def get_entity_email_from_payload(payload: dict) -> str:
    email: str | None = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token payload invalid: missing 'sub' field",
        )
    return email


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_db_session),
    user_service: UserService = Depends(get_user_service),
) -> User:
    payload = decode_token(token.credentials)
    email = get_entity_email_from_payload(payload=payload)

    try:
        user = await user_service.get_user_by_email(email)
    except NotFoundException:
        raise UnauthenticatedException("User not found")

    return user


async def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return current_user
