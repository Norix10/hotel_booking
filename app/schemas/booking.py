from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.enums.booking_enum import BookingStatus


class BookingExtraValidator:
    model_config = ConfigDict(extra="forbid")


class BookingDatesMixin(BaseModel):
    check_in: datetime | None = None
    check_out: datetime | None = None

    @model_validator(mode="after")
    def validate_dates(self):
        if (
            self.check_in is not None
            and self.check_out is not None
            and self.check_in >= self.check_out
        ):
            raise ValueError("Check-out must be after check-in")
        return self


class BookingCreateSchema(BookingDatesMixin, BookingExtraValidator):
    user_id: UUID
    room_id: int
    check_in: datetime
    check_out: datetime


class BookingUpdateSchema(BookingDatesMixin, BookingExtraValidator):
    check_in: datetime | None = Field(default=None)
    check_out: datetime | None = Field(default=None)


class BookingAdminUpdateSchema(BookingDatesMixin, BookingExtraValidator):
    user_id: UUID | None = Field(default=None)
    room_id: int | None = Field(default=None)
    check_in: datetime | None = Field(default=None)
    check_out: datetime | None = Field(default=None)
    status: BookingStatus | None = Field(default=None)


class BookingResponseSchema(BaseModel):
    id: UUID
    user_id: UUID
    room_id: int
    check_in: datetime
    check_out: datetime
    status: BookingStatus

    model_config = ConfigDict(from_attributes=True, extra="forbid")
