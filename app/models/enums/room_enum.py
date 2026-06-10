import enum


class RoomBathroomType(enum.Enum):
    shower = "shower"
    bath = "bath"
    jacuzzi = "jacuzzi"


class RoomStatusType(enum.Enum):
    available = "available"
    cleaning = "cleaning"
    occupied = "occupied"
