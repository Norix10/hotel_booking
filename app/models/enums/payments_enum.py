import enum


class PaymentMethodEnum(enum.Enum):
    card = "card"
    cash = "cash"


class PaymentStatusEnum(enum.Enum):
    success = "success"
    failed = "failed"
    refunded = "refunded"
    pending = "pending"
