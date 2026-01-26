from datetime import datetime

from src.models.rooms import RoomsORM
from src.repositories.utils import rooms_id_for_booking
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_to: datetime,
            date_from: datetime
    ):
        rooms_id = rooms_id_for_booking(hotel_id=hotel_id, date_to=date_to, date_from=date_from)
        return await self.get_filtered(self.model.id.in_(rooms_id))
