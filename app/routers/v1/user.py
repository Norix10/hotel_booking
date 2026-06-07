from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session
from app.schemas.user import UserCreateSchema, UserResponseSchema, UserSignInSchema
from app.schemas.auth import AuthResponse, AccessTokenDataSchema
from app.core.dependencies import get_current_user, get_user_service
from app.models.user import User
from app.schemas.user import UserResponseSchema, UserCreateSchema
from app.services.user import UserService

router = APIRouter(prefix="/user", tags=["users"])


@router.post("")
async def create(
    data: UserCreateSchema,
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_db_session),
):
    return await user_service.create_user(data)


@router.post("/login", response_model=AuthResponse)
async def login(
    data: UserSignInSchema,
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_db_session),
) -> AuthResponse:
    return await user_service.authenticate(data, session)


@router.get("/me", response_model=UserResponseSchema)
async def me(
    current_user: User = Security(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    return current_user
