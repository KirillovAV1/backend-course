from typing import List

from fastapi import APIRouter, Body
from fastapi.openapi.models import Example

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingRequest, BookingAdd, Booking

router = APIRouter(prefix="/bookings",
                   tags=["Бронирования"])


@router.get("/",
            summary="Получение всех бронирований",
            response_model=List[Booking])
async def get_bookings(
        db: DBDep,
):
    return await db.bookings.get_all()


@router.post("/",
             summary="Создание бронирования")
async def create_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_request: BookingRequest = Body(openapi_examples={
            "1": Example(
                summary="Пример 1",
                value={
                    "room_id": 10,
                    "date_from": "2020-04-01T09:53:43.309Z",
                    "date_to": "2020-05-01T09:53:43.309Z",
                }
            ),
            "2": Example(
                summary="Пример 2",
                value={
                    "room_id": 11,
                    "date_from": "2024-04-01T09:53:43.309Z",
                    "date_to": "2025-05-01T09:53:43.309Z",
                }
            )
        }
        ),
):
    room_data = await db.rooms.get_one_or_none(id=booking_request.room_id)
    booking_data = BookingAdd(user_id=user_id, **booking_request.model_dump(), price=room_data.price)
    booking = await db.bookings.add(booking_data)
    return {"status": "ok", "booking": booking}

@router.get("/me",
            summary="Получение бронирования текущего пользователя",
            response_model=List[Booking])
async def get_users_bookings(
        user_id: UserIdDep,
        db: DBDep,
):
    return await db.bookings.get_filtered(user_id=user_id)