from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel
from typing import Annotated

from src.database.db import async_session_maker
from src.database.db_manager import DBManager
from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="Номер страницы для пагинации")]
    per_page: Annotated[int | None, Query(None, ge=1, le=100, description="Количество отелей на странице")]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    access_token = request.cookies.get("access_token", None)
    if access_token is None:
        raise HTTPException(status_code=401, detail="Вы не указали токен доступа")
    return access_token


def get_current_user_id(token: str = Depends(get_token)):
    data = AuthService.decode_token(token)
    user_id = data["user_id"]
    return user_id


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]