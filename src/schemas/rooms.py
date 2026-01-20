from pydantic import BaseModel, Field
from src.schemas.hotels import Hotel


class RoomParams(BaseModel):
    title: str = Field(description="Название комнаты")
    description: str | None = Field(None, description="Описание комнаты")
    price: int = Field(description="Ежедневная стоимость комнаты")
    quantity: int = Field(description="Количество подобных комнат в отеле")


class RoomRequest(RoomParams):
    pass


class RoomAdd(RoomRequest):
    hotel_id: int


class Room(RoomParams):
    id: int
    hotel_id: int


class RoomResponse(RoomParams):
    id: int
    hotel_data: Hotel


class RoomPatch(BaseModel):
    title: str | None = Field(None, description="Название комнаты")
    description: str | None = Field(None, description="Описание комнаты")
    price: int | None = Field(None, description="Ежедневная стоимость комнаты")
    quantity: int | None = Field(None, description="Количество подобных комнат в отеле")
