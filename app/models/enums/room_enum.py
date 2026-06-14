import enum


class RoomBedTypeEnum(enum.Enum):
    single = "single"
    double = "double"
    queen = "queen"
    king = "king"
    twin = "twin"
    sofa = "sofa"
    bunk = "bunk"


class RoomBathroomTypeEnum(enum.Enum):
    shower = "shower"
    bath = "bath"
    jacuzzi = "jacuzzi"


class RoomStatusTypeEnum(enum.Enum):
    available = "available"
    cleaning = "cleaning"
    occupied = "occupied"
