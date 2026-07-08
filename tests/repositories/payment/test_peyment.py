import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.payment import PaymentRepository
from app.models.payment import Payment
from app.models.enums.payments_enum import PaymentMethodEnum, PaymentStatusEnum
from app.schemas.payments import PaymentFiltersSchema


@pytest.mark.asyncio
async def test_create_payment(
    prepare_db, session: AsyncSession, create_booking, create_user
):
    repo = PaymentRepository(session)
    payment = Payment(
        booking_id=create_booking.id,
        user_id=create_user.id,
        amount=200,
        payment_method=PaymentMethodEnum.cash,
        payment_status=PaymentStatusEnum.pending,
    )
    created = await repo.create(payment)
    assert created.id is not None
    assert created.amount == 200


@pytest.mark.asyncio
async def test_get_by_id(prepare_db, session: AsyncSession, create_payment):
    repo = PaymentRepository(session)
    payment = await repo.get_by_id(create_payment.id)
    assert payment.id == create_payment.id


@pytest.mark.asyncio
async def test_get_by_booking_id(
    prepare_db, session: AsyncSession, create_booking, create_payment
):
    repo = PaymentRepository(session)
    payment = await repo.get_by_booking_id(create_booking.id)
    assert payment.id == create_payment.id


@pytest.mark.asyncio
async def test_get_by_booking_id_not_found(prepare_db, session: AsyncSession):
    repo = PaymentRepository(session)
    payment = await repo.get_by_booking_id(uuid4())
    assert payment is None


@pytest.mark.asyncio
async def test_get_all_user_payments(
    prepare_db, session: AsyncSession, create_user, create_payment
):
    repo = PaymentRepository(session)
    payments = await repo.get_all_user_payments(create_user.id)
    assert len(payments) == 1


@pytest.mark.asyncio
async def test_get_all_user_payments_with_filters(
    prepare_db, session: AsyncSession, create_user, create_payment
):
    repo = PaymentRepository(session)
    matching = PaymentFiltersSchema(payment_method=PaymentMethodEnum.card)
    payments = await repo.get_all_user_payments(create_user.id, filters=matching)
    assert len(payments) == 1

    non_matching = PaymentFiltersSchema(payment_method=PaymentMethodEnum.cash)
    empty = await repo.get_all_user_payments(create_user.id, filters=non_matching)
    assert len(empty) == 0


@pytest.mark.asyncio
async def test_get_all_payments(prepare_db, session: AsyncSession, create_payment):
    repo = PaymentRepository(session)
    payments = await repo.get_all_payments()
    assert len(payments) == 1


@pytest.mark.asyncio
async def test_get_success_status(prepare_db, session: AsyncSession, create_payment):
    repo = PaymentRepository(session)
    payments = await repo.get_success_status()
    assert len(payments) == 1


@pytest.mark.asyncio
async def test_update_payment(prepare_db, session: AsyncSession, create_payment):
    repo = PaymentRepository(session)
    create_payment.payment_status = PaymentStatusEnum.refunded
    updated = await repo.update(create_payment)
    assert updated.payment_status == PaymentStatusEnum.refunded


@pytest.mark.asyncio
async def test_delete_payment(prepare_db, session: AsyncSession, create_payment):
    repo = PaymentRepository(session)
    await repo.delete(create_payment)
    deleted = await repo.get_by_id(create_payment.id)
    assert deleted is None