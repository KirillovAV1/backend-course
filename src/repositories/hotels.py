from sqlalchemy import func, select

from src.models.hotels import HotelsORM
from src.repositories.base import BaseRepository
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel

    async def get_all(self,
                      title: str | None,
                      location: str | None,
                      limit: int,
                      offset: int | None):

        query = select(self.model)
        if title:
            query = query.where(func.lower(self.model.title).contains(title.strip().lower()))
        if location:
            query = query.where(func.lower(self.model.location).contains(location.strip().lower()))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return [self.schema.model_validate(obj, from_attributes=True) for obj in result.scalars().all()]
