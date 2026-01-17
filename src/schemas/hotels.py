from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str = Field(description="Название отеля")
    location: str = Field(description="Адрес отеля")


class HotelPATCH(BaseModel):
    title: str | None = Field(None, description="Название отеля")
    location: str | None = Field(None, description="Адрес отеля")