from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Body, HTTPException, Response
from fastapi.openapi.models import Example
from pwdlib import PasswordHash
import jwt

from src.schemas.users import UserRequest, UserAdd
from src.database import async_session_maker
from src.repositories.users import UsersRepository

router = APIRouter(prefix="/auth",
                   tags=["Авторизация и аутентификация"])

password_hash = PasswordHash.recommended()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register",
             summary="Регистрация пользователя")
async def register_user(user_data: UserRequest = Body(openapi_examples={
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
    hashed_password = get_password_hash(password=user_data.password)
    new_user_data = UserAdd(email=user_data.email,
                            hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
        return {"status": "ok"}


@router.post("/login",
             summary="Аутентификация пользователя")
async def login_user(user_data: UserRequest,
                     response: Response):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=user_data.email)
        if user is None:
            raise HTTPException(status_code=401, detail=f"Пользователь с {user_data.email} не зарегистрирован")
        if not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail=f"Неверный пароль")
        access_token = create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
