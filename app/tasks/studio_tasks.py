import asyncio 

from app.core.celery_config import celery_app
from app.db.database import get_db_session
from app.repositories.booking import BookingRepository
from app.models.enums.booking_enum import BookingStatusEnum

async def _cancel_expired_logic():
    async with get_db_session() as session: 
        booking_repo = BookingRepository(session)
        expired_bookings = await booking_repo.get_expired_pending_bookins(expiration_minutes=30)

        for booking in expired_bookings: 
            booking.status = BookingStatusEnum.cancelled

        await session.commit()

@celery_app.task(name="app.task")
def cancel_expired_bookings():
    asyncio.run(_cancel_expired_logic())
