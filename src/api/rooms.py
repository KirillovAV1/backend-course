from datetime import datetime
from fastapi import APIRouter, Path, Body, HTTPException, Query
from fastapi.openapi.models import Example

from fastapi.exceptions import FastAPIDeprecationWarning
import warnings

from src.schemas.facilities import RoomFacilityRequest

warnings.simplefilter(action='ignore', category=FastAPIDeprecationWarning)

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomResponse, RoomAdd, RoomRequest, RoomPatch

router = APIRouter(prefix="/hotels",
                   tags=["Комнаты"])


@router.get("/rooms",
            summary="Все созданные комнаты")
async def get_all_rooms(db: DBDep):
    return await db.rooms.get_all()


@router.get("/{hotel_id}/rooms",
            summary="Получение комнат у отеля, доступных для бронирования")
async def get_hotels_rooms(
        db: DBDep,
        hotel_id: int = Path(description="ID отеля"),
        date_from: datetime = Query(example="2025-01-01T00:00:00", description="Дата заезда"),
        date_to: datetime = Query(example="2025-01-08T00:00:00", description="Дата выезда"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_to=date_to, date_from=date_from)


@router.get("/{hotel_id}/rooms/{room_id}",
            summary="Получение конкретной комнаты у отеля",
            response_model=RoomResponse)
async def get_hotels_room(
        db: DBDep,
        hotel_id: int = Path(description="ID отеля"),
        room_id: int = Path(description="ID комнаты")
):
    hotel_data = await db.hotels.get_one_or_none(id=hotel_id)
    room_data = await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)
    return RoomResponse(hotel_data=hotel_data, **room_data.model_dump())


@router.post("/{hotel_id}/rooms",
             summary="Добавление новой комнаты у отеля")
async def create_hotel_room(
        db: DBDep,
        hotel_id: int = Path(description="ID отеля"),
        room_data: RoomRequest = Body(openapi_examples={
            "1": Example(
                summary="Добавление комнаты 1",
                value={
                    "title": "Люкс-комната",
                    "price": 250,
                    "quantity": 2,
                    "facilities_ids": [1, 2]
                }
            ),
            "2": Example(
                summary="Добавление комнаты 2",
                value={
                    "title": "Обычная комната",
                    "description": "Комната с крысами",
                    "price": 10,
                    "quantity": 8
                }
            ),
        })
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    hotel_data = await db.hotels.get_one_or_none(id=hotel_id)
    if hotel_data is None:
        raise HTTPException(status_code=404, detail=f"Отель с id {hotel_id} не найден")
    room = await db.rooms.add(_room_data)
    _room = RoomResponse(hotel_data=hotel_data, **room.model_dump())
    rooms_facilities_ids = [RoomFacilityRequest(room_id=room.id, facility_id=facility_id)
                            for facility_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_ids)
    return {"status": "ok", "room": _room}


@router.put("/{hotel_id}/rooms/{room_id}",
            summary="Обновление всех полей комнаты")
async def update_hotel_room(
        db: DBDep,
        hotel_id: int = Path(description="ID отеля"),
        room_id: int = Path(description="ID номера"),
        room_data: RoomRequest = Body(openapi_examples={
            "1": Example(
                summary="Пример 1",
                value={
                    "title": "Повышен",
                    "price": 100,
                    "quantity": 1
                }
            ),
            "2": Example(
                summary="Пример 2",
                value={
                    "title": "Понижен",
                    "description": "Теперь здесь помойка",
                    "price": 100,
                    "quantity": 1
                }
            ),

        })
):
    await db.rooms.update(data=room_data, id=room_id, hotel_id=hotel_id)
    return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}",
              summary="Обновление выбранных полей комнаты")
async def partial_update_hotel_room(
        db: DBDep,
        hotel_id: int = Path(description="ID отеля"),
        room_id: int = Path(description="ID номера"),
        room_data: RoomPatch = Body(openapi_examples={
            "1": Example(
                summary="Пример 1",
                value={
                    "title": "Цена понижена",
                    "price": 1,
                    "quantity": 100
                }
            ),
            "2": Example(
                summary="Пример 2",
                value={
                    "description": "Цена повышена",
                    "price": 500,
                }
            ),
        })
):
    await db.rooms.update(data=room_data, id=room_id, hotel_id=hotel_id, exclude_unset=True)
    return {"status": "ok"}


@router.delete("/{hotel_id}/rooms/{room_id}/",
               summary="Удаление номера из отеля")
async def delete_hotel_room(
        db: DBDep,
        hotel_id: int = Path(description="ID отеля"),
        room_id: int = Path(description="ID номера"),
):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    return {"status": "ok"}
