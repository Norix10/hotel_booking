from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.payments import PaymentCreateSchema
from app.models.enums.booking_enum import BookingStatusEnum


class BookingExtraValidator:
    model_config = ConfigDict(extra="forbid")


class BookingDatesMixin(BaseModel):
    check_in: date | None = None
    check_out: date | None = None

    @model_validator(mode="after")
    def validate_dates(self):
        if (
            self.check_in is not None
            and self.check_out is not None
            and self.check_in >= self.check_out
        ):
            raise ValueError("Check-out date must be after check-in date")
        return self


class BookingCreateSchema(BookingDatesMixin, BookingExtraValidator):
    room_id: int
    check_in: date
    check_out: date


class BookingWithPaymentCreateSchema(BookingCreateSchema, PaymentCreateSchema):
    pass


class BookingUpdateSchema(BookingDatesMixin, BookingExtraValidator):
    check_in: date | None = Field(default=None)
    check_out: date | None = Field(default=None)


class BookingAdminUpdateSchema(BookingDatesMixin, BookingExtraValidator):
    room_id: int | None = Field(default=None)
    check_in: date | None = Field(default=None)
    check_out: date | None = Field(default=None)
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