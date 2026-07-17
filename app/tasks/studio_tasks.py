from datetime import datetime, timedelta, timezone

from app.core.celery_config import celery_app
from app.core.config import settings
from app.db.database import SyncSessionLocal
from app.models.booking import Booking
from app.models.room import Room
from app.models.enums.booking_enum import BookingStatusEnum
from app.models.enums.room_enum import RoomStatusTypeEnum


@celery_app.task(name="app.tasks.studio_tasks.cancel_expired_bookings")
def cancel_expired_bookings():
    with SyncSessionLocal() as db:
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=30)
        expired_bookings = (
            db.query(Booking)
            .filter(Booking.status == BookingStatusEnum.pending)
            .filter(Booking.created_at <= cutoff)
            .all()
        )

        for booking in expired_bookings:
            booking.status = BookingStatusEnum.cancelled

        db.commit()
        print(f"Cancelled {len(expired_bookings)} expired booking(s)")


@celery_app.task(name="app.tasks.studio_tasks.release_checked_out_rooms")
def release_checked_out_rooms():
    with SyncSessionLocal() as db:
        now = datetime.now(timezone.utc)
        rooms_to_clean = (
            db.query(Room)
            .join(Booking, Booking.room_id == Room.id)
            .filter(Booking.status == BookingStatusEnum.confirmed)
            .filter(Booking.check_out <= now)
            .filter(Room.status == RoomStatusTypeEnum.occupied)
            .all()
        )

        for room in rooms_to_clean:
            room.status = RoomStatusTypeEnum.cleaning

        db.commit()
        print(f"Released {len(rooms_to_clean)} room(s) to cleaning status")


@celery_app.task(name="app.tasks.studio_tasks.mark_rooms_available_after_cleaning")
def mark_rooms_available_after_cleaning():
    with SyncSessionLocal() as db:
        threshold = datetime.now(timezone.utc) - timedelta(
            hours=settings.CLEANING_BUFFER_HOURS
        )

        rooms_ready = (
            db.query(Room)
            .join(Booking, Booking.room_id == Room.id)
            .filter(Booking.status == BookingStatusEnum.confirmed)
            .filter(Booking.check_out <= threshold)
            .filter(Room.status == RoomStatusTypeEnum.cleaning)
            .distinct()
            .all()
        )

        for room in rooms_ready:
            room.status = RoomStatusTypeEnum.available

        db.commit()
        print(f"Marked {len(rooms_ready)} room(s) as available after cleaning")
