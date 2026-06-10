import uuid
from datetime import datetime
from sqlalchemy import Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums.booking_enum import BookingStatusEnum


class Booking(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False
    )
    check_in: Mapped[datetime] = mapped_column(nullable=False)
    check_out: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[BookingStatusEnum] = mapped_column(
        Enum(BookingStatusEnum), nullable=False
    )

    payment: Mapped[list["Payment"]] = relationship(
        back_populates="booking", cascade="all, delete-orphan"
    )
    user: Mapped["User"] = relationship(back_populates="bookings")
    room: Mapped["Room"] = relationship(back_populates="bookings")

    @property
    def total_days(self) -> int:
        return (self.check_out - self.check_in).days
