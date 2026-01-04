from fastapi import APIRouter, Query, Body, Path
from src.schemas.hotels import Hotel, HotelPATCH
from fastapi.openapi.models import Example
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Сочи", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("",
            summary="Получение списка отелей")
def get_hotels(
        pagination: PaginationDep,
        hotel_id: int | None = Query(None, description="ID отеля"),
        title: str | None = Query(None, description="Название отеля (Кириллица)"),
        name: str | None = Query(None, description="Название отеля (Латиница)"),
):
    hotels_ = []
    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        if title and hotel["title"] != title:
            continue
        if name and hotel["name"] != name:
            continue
        hotels_.append(hotel)

    end = pagination.page * pagination.per_page
    start = end - pagination.per_page
    return hotels_[start:end]


@router.post("",
             summary="Создание отеля")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "sochi": Example(
        summary="Пример для Сочи",
        value={"title": "Сочи",
               "name": "Sochi"},
    ),
    "dubai": Example(
        summary="Пример для Дубай",
        value={"title": "Дубай",
               "name": "Dubai"},
    ),
})
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
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

