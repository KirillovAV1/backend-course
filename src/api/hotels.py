from fastapi import APIRouter, Query, Body, Path, HTTPException
from fastapi.openapi.models import Example
from sqlalchemy.exc import MultipleResultsFound

from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("",
            summary="Получение списка отелей")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Адрес отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )

@router.get("/{hotel_id}",
            summary="Получение отеля по ID")
async def get_hotel(
        hotel_id: int = Path(description="ID отеля")
):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        return result


@router.post("",
             summary="Создание отеля")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
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
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}",
            summary="Обновление всех полей отеля по hotel_id")
async def full_update_hotel(
        hotel_id: int = Path(description="ID отеля"),
        hotel_data: Hotel = Body()
):
    async with async_session_maker() as session:
        try:
            result = await HotelsRepository(session).get_one_or_none(id=hotel_id)
            if result is None:
                raise HTTPException(status_code=404, detail="Объект не найден")
        except MultipleResultsFound:
            raise HTTPException(status_code=422, detail="Найдено больше одного объекта")

        await HotelsRepository(session).update(data=hotel_data, id=hotel_id)
        await session.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}",
              summary="Обновление выбранных полей по hotel_id")
async def partial_update_hotel(
        hotel_id: int = Path(description="ID отеля"),
        hotel_data: HotelPATCH = Body()
):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(data=hotel_data, id=hotel_id, exclude_unset=True)
        await session.commit()

    return {"status": "OK"}


@router.delete("/{hotel_id}",
               summary="Удаление отеля по hotel_id")
async def delete_hotel(
        hotel_id: int = Path(description="ID отеля")
):
    async with async_session_maker() as session:
        try:
            result = await HotelsRepository(session).get_one_or_none(id=hotel_id)
            if result is None:
                raise HTTPException(status_code=404, detail="Объект не найден")
        except MultipleResultsFound:
            raise HTTPException(status_code=422, detail="Найдено больше одного объекта")

        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()

    return {"status": "OK"}
