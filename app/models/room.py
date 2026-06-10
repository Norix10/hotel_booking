from sqlalchemy import Integer, ForeignKey, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums.room_enum import RoomStatusTypeEnum


class Room(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    room_name: Mapped[str] = mapped_column(String, nullable=False)
    room_type_id: Mapped[int] = mapped_column(
        ForeignKey("room_types.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[RoomStatusTypeEnum] = mapped_column(
        Enum(RoomStatusTypeEnum), nullable=False, default=RoomStatusTypeEnum.available
    )
    floor: Mapped[int] = mapped_column(Integer, nullable=False)

    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="room", cascade="all, delete-orphan"
    )

    room_types: Mapped["RoomType"] = relationship(back_populates="room")
