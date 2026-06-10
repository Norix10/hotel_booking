from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

from app.models.enums.payments_enum import PaymentMethodEnum, PaymentStatusEnum


class PaymentBaseSchema(BaseModel):
    booking_id: UUID
    amount: int = Field(ge=0)
    payment_method: PaymentMethodEnum
    payment_status: PaymentStatusEnum
    model_config = ConfigDict(extra="forbid")


class PaymentCreateSchema(BaseModel):
    amount: int = Field(ge=0)
    payment_method: PaymentMethodEnum

    model_config = ConfigDict(extra="forbid")


class PaymentUpdateSchema(BaseModel):
    id: UUID | None = Field(default=None)
    booking_id: UUID | None = Field(default=None)
    amount: int | None = Field(default=None, ge=0)
    payment_method: PaymentMethodEnum | None = Field(default=None)
    payment_status: PaymentStatusEnum | None = Field(default=None)
    model_config = ConfigDict(extra="forbid")


class PaymentResponseSchema(PaymentBaseSchema):
    id: UUID
    model_config = ConfigDict(from_attributes=True, extra="forbid")
