from pydantic import BaseModel, Field


class FacilityRequest(BaseModel):
    title: str = Field(description="Название удобства")
    description: str | None = Field(None, description="Описание удобства")


class Facility(FacilityRequest):
    id: int = Field(description="ID удобства")


class RoomFacilityRequest(BaseModel):
    room_id: int = Field(description="ID Комнаты")
    facility_id: int = Field(description="ID Удобства")


class RoomFacility(RoomFacilityRequest):
    id: int = Field(description="ID записи M2M")
