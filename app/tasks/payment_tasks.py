from uuid import UUID

from app.core.celery_config import celery_app
from app.db.database import SyncSessionLocal
from app.models.booking import Booking


@celery_app.task(name="process_payment_bg")
def process_payment_bg(user_id: UUID, booking_id: UUID):
    with SyncSessionLocal() as db:
        try:
            booking = (
                db.query(Booking)
                .filter(Booking.id == booking_id)
                .filter(Booking.user_id == user_id)
                .first()
            )

            if booking:
                booking.status = "confirmed"
                db.commit()
                print(f"Booking {booking_id} status changed as 'confirmed'")
            else:
                print(f"Booking {booking_id} is not found")

        except Exception as e:
            db.rollback()
            print(f"Database exception: {e}")
            raise e
    