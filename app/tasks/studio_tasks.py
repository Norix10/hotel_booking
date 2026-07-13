import asyncio
from datetime import datetime, timezone

from app.core.celery_config import celery_app
from app.db.database import get_db_session
from app.repositories.booking import BookingRepository
from app.models.enums.booking_enum import BookingStatusEnum
from app.models.enums.room_enum import RoomStatusTypeEnum


async def _cancel_expired_logic():
    async with get_db_session() as session:
        booking_repo = BookingRepository(session)
        expired_bookings = await booking_repo.get_expired_pending_bookins(
            expiration_minutes=30
        )

        for booking in expired_bookings:
            booking.status = BookingStatusEnum.cancelled

        await session.commit()
        print(f"Cancelled {len(expired_bookings)} expired booking(s)")


@celery_app.task(name="app.tasks.studio_tasks.cancel_expired_bookings")
def cancel_expired_bookings():
    asyncio.run(_cancel_expired_logic())


async def _release_checked_out_rooms_logic():
    async with get_db_session() as session:
        booking_repo = BookingRepository(session)
        now = datetime.now(timezone.utc)
        bookings = await booking_repo.get_confirmed_checked_out_bookings(now)

        for booking in bookings:
            booking.room.status = RoomStatusTypeEnum.cleaning

        await session.commit()
        print(f"Released {len(bookings)} room(s) to cleaning status")


@celery_app.task(name="app.tasks.studio_tasks.release_checked_out_rooms")
def release_checked_out_rooms():
    asyncio.run(_release_checked_out_rooms_logic())
