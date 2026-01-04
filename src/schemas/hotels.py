from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str = Field(description="Название отеля (Кириллица)")
    name: str = Field(description="Название отеля (Латиница)")


class HotelPATCH(BaseModel):
    title: str | None = Field(None, description="Название отеля (Кириллица)")
    name: str | None = Field(None, description="Название отеля (Латиница)")