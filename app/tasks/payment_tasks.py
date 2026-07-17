from uuid import UUID

from app.core.celery_config import celery_app
from app.db.database import SyncSessionLocal
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.enums.payments_enum import PaymentStatusEnum
from app.models.enums.booking_enum import BookingStatusEnum


@celery_app.task(name="process_payment_bg")
def process_payment_bg(user_id: UUID, booking_id: UUID):
    with SyncSessionLocal() as db:
        booking = (
            db.query(Booking)
            .filter(Booking.id == booking_id)
            .filter(Booking.user_id == user_id)
            .first()
        )

        if booking:
            booking.status = BookingStatusEnum.confirmed
            db.commit()
            print(f"Booking {booking_id} status changed to 'confirmed'")
        else:
            print(f"Booking {booking_id} is not found")


@celery_app.task(name="app.tasks.payment_tasks.auto_refund_payment")
def auto_refund_payment(booking_id: UUID):
    with SyncSessionLocal() as db:
        payment = db.query(Payment).filter(Payment.booking_id == booking_id).first()

        if not payment:
            print(f"No payment found for booking {booking_id}, nothing to refund")
            return

        if payment.payment_status == PaymentStatusEnum.refunded:
            print(f"Payment {payment.id} already refunded, skipping")
            return

        if payment.payment_status != PaymentStatusEnum.success:
            print(
                f"Payment {payment.id} has status "
                f"'{payment.payment_status}', cannot refund"
            )
            return

        payment.payment_status = PaymentStatusEnum.refunded
        db.commit()
        print(f"Payment {payment.id} for booking {booking_id} refunded")
