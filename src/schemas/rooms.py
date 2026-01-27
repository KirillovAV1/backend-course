from pydantic import BaseModel, Field

from src.schemas.facilities import Facility
from src.schemas.hotels import Hotel


class RoomParams(BaseModel):
    title: str = Field(description="Название комнаты")
    description: str | None = Field(None, description="Описание комнаты")
    price: int = Field(description="Ежедневная стоимость комнаты")
    quantity: int = Field(description="Количество подобных комнат в отеле")


class RoomRequest(RoomParams):
    facilities_ids: list[int] = Field([], description="Список удобств для комнаты")


class RoomAdd(RoomParams):
    hotel_id: int


class Room(RoomParams):
    id: int
    hotel_data: Hotel
    facilities_data: list[Facility]


class RoomPatchParams(BaseModel):
    title: str | None = Field(None, description="Название комнаты")
    description: str | None = Field(None, description="Описание комнаты")
    price: int | None = Field(None, description="Ежедневная стоимость комнаты")
    quantity: int | None = Field(None, description="Количество подобных комнат в отеле")


class RoomPatchRequest(RoomPatchParams):
    facilities_ids: list[int] | None = Field(None, description="Список удобств для комнаты")


class RoomPatch(RoomPatchParams):
    hotel_id: int
