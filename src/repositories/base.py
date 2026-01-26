from typing import List

from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *fil, **filters):
        query = (select(self.model)
                 .filter(*fil)
                 .filter_by(**filters))
        result = await self.session.execute(query)
        return [self.schema.model_validate(obj, from_attributes=True) for obj in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filters):
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        return self.schema.model_validate(obj, from_attributes=True)

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

    async def add_bulk(
            self,
            data: List[BaseModel]
    ):
        add_stmt = (
            insert(self.model)
            .values([obj.model_dump() for obj in data]))
        await self.session.execute(add_stmt)

    async def update(
            self,
            data: BaseModel,
            exclude_unset: bool = False,
            **filters
    ) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filters)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)

    async def delete(self, **filters) -> None:
        delete_stmt = delete(self.model).filter_by(**filters)
        await self.session.execute(delete_stmt)
