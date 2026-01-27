from pydantic import BaseModel, Field

class HotelAdd(BaseModel):
    title: str = Field(description="Название отеля")
    location: str = Field(description="Адрес отеля")


class Hotel(HotelAdd):
    id: int = Field(description="ID отеля")


class HotelPATCH(BaseModel):
    title: str | None = Field(None, description="Название отеля")
    location: str | None = Field(None, description="Адрес отеля")
