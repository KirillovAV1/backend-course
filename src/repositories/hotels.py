from datetime import datetime
from typing import List

from sqlalchemy import func, select

from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_id_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel

    async def get_filtered_by_time(
            self,
            date_to: datetime,
            date_from: datetime,
            title: str | None,
            location: str | None,
            limit: int,
            offset: int | None
    ) -> List[Hotel]:
        rooms_id = rooms_id_for_booking(date_to=date_to, date_from=date_from)

        hotels_id = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .where(RoomsORM.id.in_(rooms_id))
            .group_by(RoomsORM.hotel_id)
        )

        query = (
            select(self.model)
            .select_from(self.model)
            .where(self.model.id.in_(hotels_id))
        )

        if location:
            query = query.where(func.lower(self.model.location).contains(location.strip().lower()))
        if title:
            query = query.where(func.lower(self.model.title).contains(title.strip().lower()))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return [self.schema.model_validate(obj, from_attributes=True) for obj in result.scalars().all()]
