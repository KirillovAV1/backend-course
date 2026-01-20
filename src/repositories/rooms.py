from typing import List

from pydantic import BaseModel
from sqlalchemy import insert, select

from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_all(self, **filters) -> List[Room]:
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        return [self.schema.model_validate(obj, from_attributes=True) for obj in result.scalars().all()]

    async def add(
            self,
            data: BaseModel
    ):
        add_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model))
        result = await self.session.execute(add_stmt)
        obj = result.scalars().one()
        return self.schema.model_validate(obj, from_attributes=True)
