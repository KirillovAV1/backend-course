from fastapi import Depends, Query
from pydantic import BaseModel
from typing import Annotated

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="Номер страницы для пагинации")]
    per_page: Annotated[int | None, Query(None, ge=1, le=100, description="Количество отелей на странице")]


PaginationDep = Annotated[PaginationParams, Depends()]
