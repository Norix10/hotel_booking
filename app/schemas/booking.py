from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.payments import PaymentCreateSchema
from app.models.enums.booking_enum import BookingStatusEnum


class BookingExtraValidator:
    model_config = ConfigDict(extra="forbid")


class BookingDatesMixin(BaseModel):
    check_in: datetime | None = None
    check_out: datetime | None = None

    @model_validator(mode="before")
    def make_datetimes_aware(cls, values):
        if not isinstance(values, dict):
            return values

        for field in ("check_in", "check_out"):
            value = values.get(field)
            if isinstance(value, datetime) and value.tzinfo is None:
                values[field] = value.replace(tzinfo=timezone.utc)

        return values

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
    room_id: int
    check_in: datetime
    check_out: datetime


class BookingWithPaymentCreateSchema(BookingCreateSchema, PaymentCreateSchema):
    pass


class BookingUpdateSchema(BookingDatesMixin, BookingExtraValidator):
    check_in: datetime | None = Field(default=None)
    check_out: datetime | None = Field(default=None)


class BookingAdminUpdateSchema(BookingDatesMixin, BookingExtraValidator):
    user_id: UUID | None = Field(default=None)
    room_id: int | None = Field(default=None)
    check_in: datetime | None = Field(default=None)
    check_out: datetime | None = Field(default=None)
    status: BookingStatusEnum | None = Field(default=None)


class BookingAdminFilterSchema(BookingAdminUpdateSchema):
    pass

class BookingResponseSchema(BaseModel):
    id: UUID
    user_id: UUID
    room_id: int
    check_in: datetime
    check_out: datetime
    status: BookingStatusEnum

    model_config = ConfigDict(from_attributes=True, extra="forbid")
