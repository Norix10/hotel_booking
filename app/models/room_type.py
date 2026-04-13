from sqlalchemy import String, Integer, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums.room_enum import RoomBathroomType


class RoomType(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    base_price: Mapped[int] = mapped_column(Integer, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    bed_type: Mapped[str] = mapped_column(String(30), nullable=False)
    role: Mapped[RoomBathroomType] = mapped_column(
        Enum(RoomBathroomType), nullable=False
    )
    area_sq_m: Mapped[str] = mapped_column(Integer, nullable=False)
    has_ac: Mapped[bool] = mapped_column(Boolean, nullable=False)  # air conditioner
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)

    room: Mapped[list["Room"]] = relationship(
        back_populates="room_type", cascade="all, delete-orphan"
    )
