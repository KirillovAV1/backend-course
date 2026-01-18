from fastapi import APIRouter, Query, Body, Path
from fastapi.openapi.models import Example
from sqlalchemy import insert, select, update, delete, func

from src.models.hotels import HotelsORM
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
        add_hotel_stmt = insert(HotelsORM).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router.put("/{hotel_id}",
            summary="Обновление всех полей отеля по hotel_id")
def full_update_hotel(
        hotel_id: int = Path(description="ID отеля"),
        hotel_data: Hotel = Body()
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.patch("/{hotel_id}",
              summary="Обновление выбранных полей по hotel_id")
def partial_update_hotel(
        hotel_id: int = Path(description="ID отеля"),
        hotel_data: HotelPATCH = Body()
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.delete("/{hotel_id}",
               summary="Удаление отеля по hotel_id")
def delete_hotel(
        hotel_id: int = Path(description="ID отеля")
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
