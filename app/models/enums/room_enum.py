from enum import Enum

class RoomBathroomType(Enum):
    shower = "shower"
    bath = "bath"
    jacuzzi = "jacuzzi"

class RoomStatusType(Enum):
    available = "available"
    cleaning = "cleaning"
    occupied = "occupied"