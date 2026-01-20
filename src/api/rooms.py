from fastapi import APIRouter, Path, Body, HTTPException
from fastapi.openapi.models import Example

from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomResponse, RoomAdd, RoomRequest, RoomPatch

router = APIRouter(prefix="/hotels",
                   tags=["Комнаты"])


@router.get("/rooms",
            summary="Все созданные комнаты")
async def get_all_rooms():
    async with async_session_maker() as session:
        result = await RoomsRepository(session).get_all()
        return result


@router.get("/{hotel_id}/rooms",
            summary="Получение списка комнат у отеля")
async def get_hotels_rooms(
        hotel_id: int = Path(description="ID отеля")
):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).get_all(hotel_id=hotel_id)
        return result


@router.get("/{hotel_id}/rooms/{room_id}",
            summary="Получение конкретной комнаты у отеля",
            response_model=RoomResponse)
async def get_hotels_room(
        hotel_id: int = Path(description="ID отеля"),
        room_id: int = Path(description="ID комнаты")
):
    async with async_session_maker() as session:
        hotel_data = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        result = await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)
        _result = RoomResponse(hotel_data=hotel_data, **result.model_dump())
        return _result


@router.post("/{hotel_id}/rooms",
             summary="Добавление новой комнаты у отеля")
async def create_hotel_room(
        hotel_id: int = Path(description="ID отеля"),
        room_data: RoomRequest = Body(openapi_examples={
            "1": Example(
                summary="Добавление комнаты 1",
                value={
                    "title": "Люкс-комната",
                    "price": 250,
                    "quantity": 2

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
    async with async_session_maker() as session:
        hotel_data = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        if hotel_data is None:
            raise HTTPException(status_code=404, detail=f"Отель с id {hotel_id} не найден")
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()
        _room = RoomResponse(hotel_data=hotel_data, **room.model_dump())
        return {"status": "ok", "room": _room}


@router.put("/{hotel_id}/rooms/{room_id}",
            summary="Обновление всех полей комнаты")
async def update_hotel_room(
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
    async with async_session_maker() as session:
        await RoomsRepository(session).update(data=room_data, id=room_id, hotel_id=hotel_id)
        await session.commit()
        return {"status": "ok"}

@router.patch("/{hotel_id}/rooms/{room_id}",
              summary="Обновление выбранных полей комнаты")
async def partial_update_hotel_room(
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
    async with async_session_maker() as session:
        await RoomsRepository(session).update(data=room_data, id=room_id, hotel_id=hotel_id, exclude_unset=True)
        await session.commit()
        return {"status": "ok"}


@router.delete("/{hotel_id}/rooms/{room_id}/",
               summary="Удаление номера из отеля")
async def delete_hotel_room(
        hotel_id: int = Path(description="ID отеля"),
        room_id: int = Path(description="ID номера"),
):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
        return {"status": "ok"}
