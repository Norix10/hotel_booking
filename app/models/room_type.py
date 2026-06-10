from sqlalchemy import String, Integer, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums.room_enum import RoomBathroomTypeEnum


class RoomType(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    base_price: Mapped[int] = mapped_column(Integer, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    bed_type: Mapped[str] = mapped_column(String(30), nullable=False)
    bathroom_type: Mapped[RoomBathroomTypeEnum] = mapped_column(
        Enum(RoomBathroomTypeEnum), nullable=False
    )
    area_sq_m: Mapped[int] = mapped_column(Integer, nullable=False)
    has_ac: Mapped[bool] = mapped_column(Boolean, nullable=False)  # air conditioner
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)

    room: Mapped[list["Room"]] = relationship(
        back_populates="room_types", cascade="all, delete-orphan"
    )
