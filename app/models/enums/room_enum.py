import enum


class RoomBathroomTypeEnum(enum.Enum):
    shower = "shower"
    bath = "bath"
    jacuzzi = "jacuzzi"


class RoomStatusTypeEnum(enum.Enum):
    available = "available"
    cleaning = "cleaning"
    occupied = "occupied"
