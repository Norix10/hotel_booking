import uuid
from sqlalchemy import Integer, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums.payments_enum import PaymentMethodEnum, PaymentStatusEnum

class Payment(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, nullable=False, default=uuid.uuid4)
    booking_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("booking.id", ondelete="CASCADE"), nullable=False)
    amout: Mapped[int] = mapped_column(Integer, nullable=False)
    payment_method: Mapped[PaymentMethodEnum] = mapped_column(Enum(PaymentMethodEnum), nullable=False)
    payment_status: Mapped[PaymentStatusEnum] = mapped_column(Enum(PaymentStatusEnum), nullable=False)    

    booking: Mapped["Booking"] = relationship(back_populates="payment")
    

