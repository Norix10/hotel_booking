from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

from app.models.enums.room_enum import RoomStatusTypeEnum


class RoomBaseSchema(BaseModel):
    room_name: str
    room_type_id: int
    status: RoomStatusTypeEnum
    floor: int
    model_config = ConfigDict(extra="forbid")


class RoomResponseSchema(RoomBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class RoomCreateSchema(RoomBaseSchema):
    pass


class RoomUpdateSchema(BaseModel):
    room_name: str | None = Field(default=None)
    room_type_id: int | None = Field(default=None)
    status: RoomStatusTypeEnum | None = Field(default=None)
    floor: int | None = Field(default=None)
