from datetime import datetime
from pydantic import BaseModel, Field


class BookingRequest(BaseModel):
    room_id: int = Field(description="ID комнаты")
    date_from: datetime = Field(description="Дата заезда")
    date_to: datetime = Field(description="Дата выезда")


class BookingAdd(BookingRequest):
    user_id: int = Field(description="ID пользователя")
    price: int = Field(description="Цена за ночь в отеле")


class Booking(BookingAdd):
    id: int = Field(description="ID заказа")
