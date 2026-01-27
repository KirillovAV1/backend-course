from fastapi import APIRouter, Body
from fastapi.openapi.models import Example

from src.schemas.facilities import FacilityRequest, Facility
from src.api.dependencies import DBDep

router = APIRouter(
    prefix="/facilities",
    tags=["Удобства"]
)


@router.get("",
            summary="Получение списка удобств",
            response_model=list[Facility])
async def get_facilities(
        db: DBDep,
):
    return await db.facilities.get_all()


@router.post("",
             summary="Создание удобства")
async def create_facility(
        db: DBDep,
        facility_data: FacilityRequest = Body(openapi_examples={
            "1": Example(
                summary="Пример 1",
                value={
                    "title": "Вид на море",
                    "description": "",
                }
            ),
            "2": Example(
                summary="Пример 2",
                value={
                    "title": "Бассейн в комнате",
                    "description": "Личный надувной бассейн, который принесут работники отеля. Наберут и надуют",
                }
            )
        })
):
    facility = await db.facilities.add(facility_data)
    return {"status": "ok", "data": facility}
