import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.services.payments import PaymentsService
from app.repositories.payment import PaymentRepository
from app.repositories.booking import BookingRepository
from app.schemas.payments import PaymentCreateSchema, PaymentUpdateSchema
from app.models.enums.payments_enum import PaymentMethodEnum, PaymentStatusEnum
from app.models.enums.booking_enum import BookingStatusEnum


def build_service(session: AsyncSession) -> PaymentsService:
    return PaymentsService(PaymentRepository(session), BookingRepository(session))


@pytest.mark.asyncio
async def test_create_payment(
    prepare_db, session: AsyncSession, create_user, create_booking
):
    service = build_service(session)
    data = PaymentCreateSchema(payment_method=PaymentMethodEnum.card)
    payment = await service.create_payment(
        create_booking.id, data, user_id=create_user.id
    )
    assert payment.booking_id == create_booking.id
    assert payment.payment_status == PaymentStatusEnum.success


@pytest.mark.asyncio
async def test_create_payment_booking_not_found(
    prepare_db, session: AsyncSession, create_user
):
    service = build_service(session)
    data = PaymentCreateSchema(payment_method=PaymentMethodEnum.card)
    with pytest.raises(HTTPException) as exc_info:
        await service.create_payment(uuid4(), data, user_id=create_user.id)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_payment_wrong_user(
    prepare_db, session: AsyncSession, create_booking
):
    service = build_service(session)
    data = PaymentCreateSchema(payment_method=PaymentMethodEnum.card)
    with pytest.raises(HTTPException) as exc_info:
        await service.create_payment(create_booking.id, data, user_id=uuid4())
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_create_payment_duplicate(
    prepare_db, session: AsyncSession, create_user, create_booking
):
    service = build_service(session)
    data = PaymentCreateSchema(payment_method=PaymentMethodEnum.card)
    await service.create_payment(create_booking.id, data, user_id=create_user.id)
    with pytest.raises(HTTPException) as exc_info:
        await service.create_payment(create_booking.id, data, user_id=create_user.id)
    assert exc_info.value.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_create_payment_cancelled_booking(
    prepare_db, session: AsyncSession, create_user, create_booking
):
    create_booking.status = BookingStatusEnum.cancelled
    await session.commit()
    service = build_service(session)
    data = PaymentCreateSchema(payment_method=PaymentMethodEnum.card)
    with pytest.raises(HTTPException) as exc_info:
        await service.create_payment(create_booking.id, data, user_id=create_user.id)
    assert exc_info.value.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_get_payment_by_id(prepare_db, session: AsyncSession, create_payment):
    service = build_service(session)
    payment = await service.get_payment_by_id(create_payment.id)
    assert payment.id == create_payment.id


@pytest.mark.asyncio
async def test_get_payment_by_id_not_found(prepare_db, session: AsyncSession):
    service = build_service(session)
    with pytest.raises(HTTPException) as exc_info:
        await service.get_payment_by_id(uuid4())
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_all_user_payments(
    prepare_db, session: AsyncSession, create_user, create_payment
):
    service = build_service(session)
    payments = await service.get_all_user_payments(create_user.id)
    assert len(payments) == 1


@pytest.mark.asyncio
async def test_admin_get_all_payments(prepare_db, session: AsyncSession, create_payment):
    service = build_service(session)
    payments = await service.admin_get_all_payments()
    assert len(payments) == 1


@pytest.mark.asyncio
async def test_update_payment(prepare_db, session: AsyncSession, create_payment):
    service = build_service(session)
    data = PaymentUpdateSchema(payment_status=PaymentStatusEnum.refunded)
    updated = await service.update_payment(create_payment.id, data)
    assert updated.payment_status == PaymentStatusEnum.refunded


@pytest.mark.asyncio
async def test_delete_payment(prepare_db, session: AsyncSession, create_payment):
    service = build_service(session)
    await service.delete_payment(create_payment.id)
    with pytest.raises(HTTPException):
        await service.get_payment_by_id(create_payment.id)