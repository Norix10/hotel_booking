from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.schemas.user import (
    UserResponseSchema,
    UserUpdateSchema,
    UserCreateSchema,
    UserSignInSchema,
)
from app.schemas.auth import AccessTokenDataSchema, AuthResponse
from app.utils.security import get_password_hash, verify_password
from app.services.auth import create_access_token
from app.repositories.user import UserRepository
from app.models.user import User


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def _get_user_or_404(self, user_id: UUID) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User is not found"
            )
        return user

    async def get_user_by_email(self, email: str) -> User:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    async def validate_emails(self, email: str):
        if await self.user_repo.get_by_email(email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email is busy"
            )

    async def get_user_by_id(self, user_id: UUID) -> UserResponseSchema:
        user = await self._get_user_or_404(user_id)
        return UserResponseSchema.model_validate(user)

    async def create_user(self, data: UserCreateSchema) -> UserResponseSchema:
        await self.validate_emails(data.email)

        user = User(
            name=data.name,
            email=data.email,
            hashed_password=get_password_hash(data.password),
        )
        return await self.user_repo.create(user)

    async def authenticate(self, data: UserSignInSchema) -> AuthResponse:
        user = await self.user_repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User is not found"
            )

        token_data = AccessTokenDataSchema(sub=user.email)
        access_token = create_access_token(data=token_data)
        return AuthResponse(access_token=access_token, token_type="bearer")

    async def update_user(
        self, user_id: UUID, user_data: UserUpdateSchema
    ) -> UserResponseSchema:
        user = await self._get_user_or_404(user_id)
        for field, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        updated_user = await self.user_repo.update(user)
        return UserResponseSchema.model_validate(updated_user)

    async def delete_user(self, user_id: UUID) -> None:
        user = await self._get_user_or_404(user_id)
        await self.user_repo.delete(user)
