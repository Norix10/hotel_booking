from datetime import datetime, timedelta, timezone

from app.core.celery_config import celery_app
from app.db.database import SyncSessionLocal
from app.models.booking import Booking
from app.models.room import Room
from app.models.enums.booking_enum import BookingStatusEnum
from app.models.enums.room_enum import RoomStatusTypeEnum


@celery_app.task(name="app.tasks.studio_tasks.cancel_expired_bookings")
def cancel_expired_bookings():
    with SyncSessionLocal() as db:
        try:
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

        except Exception as e:
            db.rollback()
            print(f"Database exception: {e}")
            raise e


@celery_app.task(name="app.tasks.studio_tasks.release_checked_out_rooms")
def release_checked_out_rooms():
    with SyncSessionLocal() as db:
        try:
            now = datetime.now(timezone.utc)
            bookings = (
                db.query(Booking)
                .join(Room, Booking.room_id == Room.id)
                .filter(Booking.status == BookingStatusEnum.confirmed)
                .filter(Booking.check_out <= now)
                .filter(Room.status == RoomStatusTypeEnum.occupied)
                .all()
            )

            for booking in bookings:
                booking.room.status = RoomStatusTypeEnum.cleaning

            db.commit()
            print(f"Released {len(bookings)} room(s) to cleaning status")

        except Exception as e:
            db.rollback()
            print(f"Database exception: {e}")
            raise e
