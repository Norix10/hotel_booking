from enum import Enum


class PaymentMethodEnum(Enum):
    card = "card"
    cash = "cash"

class PaymentStatusEnum(Enum):
    success = "success"
    failed = "failed"
    refunded = "refunded"
    
