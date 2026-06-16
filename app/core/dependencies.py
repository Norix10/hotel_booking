import jwt
from jwt import InvalidTokenError
from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.config import settings
from app.db.database import get_db_session
from app.utils.exceptions import NotFoundException, UnauthenticatedException
from app.models.enums.user_enum import UserRoleEnum

from app.repositories.user import UserRepository
from app.repositories.booking import BookingRepository
from app.repositories.room import RoomRepository
from app.repositories.payment import PaymentRepository
from app.repositories.room_type import RoomTypeRepository

from app.services.user import UserService
from app.services.booking import BookingService
from app.services.booking_payments import BookingPaymentService
from app.services.room import RoomService
from app.services.payments import PaymentsService
from app.services.room_type import RoomTypesService

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


async def get_room_repo(
    session: AsyncSession = Depends(get_db_session),
) -> RoomRepository:
    return RoomRepository(session)


async def get_room_service(room_repo: RoomRepository = Depends(get_room_repo)):
    return RoomService(room_repo)


async def get_payment_repo(
    session: AsyncSession = Depends(get_db_session),
) -> PaymentRepository:
    return PaymentRepository(session)


async def get_booking_repo(
    session: AsyncSession = Depends(get_db_session),
) -> BookingRepository:
    return BookingRepository(session)


async def get_booking_service(
    session: AsyncSession = Depends(get_db_session),
) -> BookingService:
    return BookingService(
        BookingRepository(session),
        RoomRepository(session),
        PaymentRepository(session),
    )


async def get_payment_service(
    session: AsyncSession = Depends(get_db_session),
) -> PaymentsService:
    return PaymentsService(PaymentRepository(session), BookingRepository(session))


async def get_booking_payment_service(
    session: AsyncSession = Depends(get_db_session),
    booking_servive: BookingService = Depends(get_booking_service),
) -> BookingPaymentService:
    return BookingPaymentService(
        BookingRepository(session),
        PaymentRepository(session),
        RoomRepository(session),
        booking_service = booking_servive
    )


async def get_room_type_repo(session: AsyncSession = Depends(get_db_session)):
    return RoomTypeRepository(session)


async def get_room_type_service(
    room_types_repo: RoomTypeRepository = Depends(get_room_type_repo),
) -> RoomTypesService:
    return RoomTypesService(room_types_repo)


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
    if current_user.role != UserRoleEnum.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return current_user
