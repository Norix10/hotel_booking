import enum


class BookingStatusEnum(enum.Enum):
    confirmed = "confirmed"
    pending = "pending"
    cancelled = "cancelled"
