from typing import List
from pydantic import BaseModel, Field
from src.schemas.hotels import Hotel


class RoomParams(BaseModel):
    title: str = Field(description="Название комнаты")
    description: str | None = Field(None, description="Описание комнаты")
    price: int = Field(description="Ежедневная стоимость комнаты")
    quantity: int = Field(description="Количество подобных комнат в отеле")


class RoomPatchParams(BaseModel):
    title: str | None = Field(None, description="Название комнаты")
    description: str | None = Field(None, description="Описание комнаты")
    price: int | None = Field(None, description="Ежедневная стоимость комнаты")
    quantity: int | None = Field(None, description="Количество подобных комнат в отеле")


class RoomRequest(RoomParams):
    facilities_ids: List[int] = Field([], description="Список удобств для комнаты")


class RoomResponse(RoomParams):
    id: int
    hotel_data: Hotel


class RoomAdd(RoomParams):
    hotel_id: int


class Room(RoomParams):
    id: int
    hotel_id: int


class RoomPatchRequest(RoomPatchParams):
    facilities_ids: List[int] | None = Field(None, description="Список удобств для комнаты")

class RoomPatch(RoomPatchParams):
    hotel_id: int

