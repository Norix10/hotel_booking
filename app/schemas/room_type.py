from pydantic import BaseModel, Field, ConfigDict

from app.models.enums.room_enum import RoomBathroomTypeEnum, RoomBedTypeEnum


class RoomTypeBaseSchema(BaseModel):
    name: str = Field(min_length=3, max_length=40)
    base_price: int = Field(min=0)
    capacity: int = Field(min=0)
    bed_type: RoomBedTypeEnum
    bathroom_type: RoomBathroomTypeEnum
    area_sq_m: int = Field(ge=3, le=40)
    has_ac: bool
    has_wifi: bool

    model_config = ConfigDict(from_attributes=True)


class RoomTypeResposeSchema(RoomTypeBaseSchema):
    id: int


class RoomTypeCreateSchema(RoomTypeBaseSchema):
    pass


class RoomTypeUpdateSchema(BaseModel):
    id: int | None = Field(default=None)
    name: str | None = Field(default=None, min_length=3, max_length=40)
    base_price: int | None = Field(default=None, min=0)
    capacity: int | None = Field(default=None, min=0)
    bed_type: RoomBedTypeEnum | None = Field(default=None)
    bathroom_type: RoomBathroomTypeEnum | None = Field(default=None)
    area_sq_m: int | None = Field(default=None, ge=3, le=40)
    has_ac: bool | None = Field(default=None)
    has_wifi: bool | None = Field(default=None)
