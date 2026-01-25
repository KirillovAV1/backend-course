from fastapi import APIRouter, Query, Body, Path, HTTPException
from fastapi.openapi.models import Example
from sqlalchemy.exc import MultipleResultsFound

from src.schemas.hotels import HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("",
            summary="Получение списка отелей")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Адрес отеля"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get("/{hotel_id}",
            summary="Получение отеля по ID")
async def get_hotel(
        db: DBDep,
        hotel_id: int = Path(description="ID отеля"),
):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("",
             summary="Создание отеля")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples={
            "sochi": Example(
                summary="Пример отеля для Сочи",
                value={"title": "Звездочка",
                       "location": "Сочи, ул. Ленина"},
            ),
            "dubai": Example(
                summary="Пример отеля для Дубай",
                value={"title": "Relax",
                       "location": "Dubai, Apple street"},
            ),
        })
):
    hotel = await db.hotels.add(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}",
            summary="Обновление всех полей отеля по hotel_id")
async def full_update_hotel(
        db: DBDep,
        hotel_id: int = Path(description="ID отеля"),
        hotel_data: HotelAdd = Body()
):
    try:
        result = await db.hotels.get_one_or_none(id=hotel_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Объект не найден")
    except MultipleResultsFound:
        raise HTTPException(status_code=422, detail="Найдено больше одного объекта")

    await db.hotels.update(data=hotel_data, id=hotel_id)
    return {"status": "OK"}


@router.patch("/{hotel_id}",
              summary="Обновление выбранных полей по hotel_id")
async def partial_update_hotel(
        db: DBDep,
        hotel_id: int = Path(description="ID отеля"),
        hotel_data: HotelPATCH = Body()
):
    try:
        result = await db.hotels.get_one_or_none(id=hotel_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Объект не найден")
    except MultipleResultsFound:
        raise HTTPException(status_code=422, detail="Найдено больше одного объекта")

    await db.hotels.update(data=hotel_data, id=hotel_id, exclude_unset=True)
    return {"status": "OK"}


@router.delete("/{hotel_id}",
               summary="Удаление отеля по hotel_id")
async def delete_hotel(
        db: DBDep,
        hotel_id: int = Path(description="ID отеля")
):
    try:
        result = await db.hotels.get_one_or_none(id=hotel_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Объект не найден")
    except MultipleResultsFound:
        raise HTTPException(status_code=422, detail="Найдено больше одного объекта")

    await db.hotels.delete(id=hotel_id)
    return {"status": "OK"}
