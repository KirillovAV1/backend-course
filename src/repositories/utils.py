from datetime import datetime
from sqlalchemy import func, select

from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM


def rooms_id_for_booking(
        date_to: datetime,
        date_from: datetime,
        hotel_id: int | None = None,
):
    booked_on_date = (
        select(
            BookingsORM.room_id,
            func.count(BookingsORM.room_id).label("reserved_rooms")
        )
        .select_from(BookingsORM)
        .where(BookingsORM.date_to > date_from,
               BookingsORM.date_from < date_to)
        .group_by(BookingsORM.room_id)
        .cte("booked_on_date")
    )

    rooms_left = (
        select(
            RoomsORM.id,
            func.coalesce(RoomsORM.quantity - booked_on_date.c.reserved_rooms, RoomsORM.quantity)
            .label("free_rooms")
        )
        .select_from(RoomsORM)
        .outerjoin(booked_on_date, RoomsORM.id == booked_on_date.c.room_id)
        .cte("rooms_left")
    )

    rooms_by_hotel_id = (select(RoomsORM.id)
                         .select_from(RoomsORM))

    if hotel_id is not None:
        rooms_by_hotel_id = (rooms_by_hotel_id.
                             where(RoomsORM.hotel_id == hotel_id))

    rooms_by_hotel_id = rooms_by_hotel_id.subquery()

    rooms_id = (
        select(
            rooms_left.c.id,
        )
        .select_from(rooms_left)
        .where(
            rooms_left.c.free_rooms > 0,
            rooms_left.c.id.in_(select(rooms_by_hotel_id))
        )
    )
    return rooms_id
