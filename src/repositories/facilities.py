from sqlalchemy import delete, select, insert

from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    schema = RoomFacility

    async def set_facilities(self,
                             room_id, facilities_ids=list[int]):
        query = select(self.model.facility_id).filter_by(room_id=room_id)
        result = await self.session.execute(query)
        old_facilities_ids = result.scalars().all()

        ids_to_insert = list(set(facilities_ids) - set(old_facilities_ids))
        ids_to_delete = list(set(old_facilities_ids) - set(facilities_ids))

        if ids_to_insert:
            add_stmt = (
                insert(self.model)
                .values([{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_insert])
            )
            await self.session.execute(add_stmt)

        if ids_to_delete:
            delete_stmt = (
                delete(self.model)
                .where(self.model.room_id == room_id,
                       self.model.facility_id.in_(ids_to_delete))
            )
            await self.session.execute(delete_stmt)
