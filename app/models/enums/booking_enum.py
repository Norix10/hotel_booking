import enum

class BookingStatus(enum.Enum):
    confirmed = "confirmed"
    pending = "pending"
    cancelled = "cancelled"