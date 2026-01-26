from pydantic import BaseModel, Field


class FacilityRequest(BaseModel):
    title: str = Field(description="Название удобства")
    description: str | None = Field(None, description="Описание удобства")

class Facility(FacilityRequest):
    id: int = Field(description="ID удобства")
