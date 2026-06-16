from uuid import UUID
from typing import TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.repositories.base import BaseRepository
from app.models.payment import Payment
from app.models.enums.payments_enum import PaymentStatusEnum, PaymentMethodEnum


class PaymentRepository(BaseRepository[Payment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Payment, session)

    async def get_by_booking_id(self, booking_id: UUID) -> Payment | None:
        result = await self.session.execute(
            select(Payment).where(Payment.booking_id == booking_id)
        )
        return result.scalar_one_or_none()

    async def get_all_user_payments(
        self, user_id: UUID, skip: int = 0, limit: int = 10
    ) -> list[Payment]:
        result = await self.session.execute(
            select(Payment).where(Payment.user_id == user_id).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_all_payments(self, skip: int = 0, limit: int = 10) -> list[Payment]:
        result = await self.session.execute(select(Payment).offset(skip).limit(limit))
        return result.scalars().all()

    # __________________________________________________
    async def get_success_status(self) -> list[Payment]:
        result = await self.session.execute(
            select(Payment).where(Payment.payment_status == PaymentStatusEnum.success)
        )
        return result.scalars().all()

    async def get_failed_status(self) -> list[Payment]:
        result = await self.session.execute(
            select(Payment).where(Payment.payment_status == PaymentStatusEnum.failed)
        )
        return result.scalars().all()

    async def get_refunded_status(self) -> list[Payment]:
        result = await self.session.execute(
            select(Payment).where(Payment.payment_status == PaymentStatusEnum.refunded)
        )
        return result.scalars().all()

    async def get_payment_method_card(self) -> list[Payment]:
        result = await self.session.execute(
            select(Payment).where(Payment.payment_method == PaymentMethodEnum.card)
        )
        return result.scalars().all()

    async def get_payment_method_cash(self) -> list[Payment]:
        result = await self.session.execute(
            select(Payment).where(Payment.payment_method == PaymentMethodEnum.cash)
        )
        return result.scalars().all()
