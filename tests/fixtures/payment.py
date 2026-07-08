import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment
from app.models.enums.payments_enum import PaymentMethodEnum, PaymentStatusEnum


@pytest.fixture()
def payment_payload():
    return {
        "payment_method": PaymentMethodEnum.card,
    }


@pytest_asyncio.fixture(scope="function")
async def create_payment(
    session: AsyncSession, create_booking, create_user
) -> Payment:
    payment = Payment(
        booking_id=create_booking.id,
        user_id=create_user.id,
        amount=300,
        payment_method=PaymentMethodEnum.card,
        payment_status=PaymentStatusEnum.success,
    )
    session.add(payment)
    await session.commit()
    await session.refresh(payment)
    return payment