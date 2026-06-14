from uuid import UUID
from fastapi import APIRouter, Depends, Security, status

from app.schemas.user import (
    UserCreateSchema,
    UserResponseSchema,
    UserSignInSchema,
    UserUpdateSchema,
)
from app.schemas.auth import AuthResponse
from app.core.dependencies import get_current_user, get_user_service, get_current_admin
from app.models.user import User
from app.services.user import UserService

router = APIRouter(prefix="/user", tags=["users"])


@router.post("", response_model=UserResponseSchema)
async def register(
    data: UserCreateSchema,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.create_user(data)


@router.post("/signin", response_model=AuthResponse)
async def signin(
    data: UserSignInSchema,
    user_service: UserService = Depends(get_user_service),
) -> AuthResponse:
    return await user_service.authenticate(data)


@router.get("/me", response_model=UserResponseSchema)
async def get_me(
    current_user: User = Security(get_current_user),
) -> UserResponseSchema:
    return current_user


@router.get("/users", response_model=list[UserResponseSchema])
async def get_users_list(
    current_admin: User = Security(get_current_admin),
    user_service: UserService = Depends(get_user_service),
) -> list[UserResponseSchema]:
    return await user_service.get_all_users()


@router.patch("/", response_model=UserResponseSchema)
async def update_me(
    data: UserUpdateSchema,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Security(get_current_user),
) -> UserResponseSchema:
    return await user_service.update_user(current_user.id, data)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    user_service: UserService = Depends(get_user_service),
    current_user: User = Security(get_current_user),
):
    await user_service.delete_user(current_user.id)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(
    user_id: UUID,
    current_admin: User = Security(get_current_admin),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.delete_user(user_id)
