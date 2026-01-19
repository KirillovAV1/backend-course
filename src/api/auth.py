from fastapi import APIRouter, Body
from fastapi.openapi.models import Example
from pwdlib import PasswordHash

from src.schemas.users import UserRequestAdd, UserAdd
from src.database import async_session_maker
from src.repositories.users import UsersRepository

router = APIRouter(prefix="/auth",
                   tags=["Авторизация и аутентификация"])

password_hash = PasswordHash.recommended()


@router.post("/register",
             summary="Регистрация пользователя")
async def register_user(user_data: UserRequestAdd = Body(openapi_examples={
    "user1": Example(
        summary="Пример 1",
        value={"email": "test_max@gmail.com",
               "password": "qwerty123"}
    ),
    "user2": Example(
        summary="Пример 2",
        value={"email": "user_mail@yandex.com",
               "password": "passw0rd"}
    )
})):
    hashed_password = password_hash.hash(password=user_data.password)
    print(hashed_password)
    new_user_data = UserAdd(email=user_data.email,
                            hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
        return {"status": "ok"}
