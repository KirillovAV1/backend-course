from fastapi import APIRouter, Body, HTTPException, Response
from fastapi.openapi.models import Example

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequest, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth",
                   tags=["Авторизация и аутентификация"])


@router.post("/register",
             summary="Регистрация пользователя")
async def register_user(db: DBDep,
                        user_data: UserRequest = Body(openapi_examples={
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
    hashed_password = AuthService().get_password_hash(user_data.password)
    new_user_data = UserAdd(email=user_data.email,
                            hashed_password=hashed_password)
    await db.users.add(new_user_data)
    return {"status": "ok"}


@router.post("/login",
             summary="Аутентификация пользователя")
async def login_user(db: DBDep,
                     user_data: UserRequest,
                     response: Response):
    user = await db.users.get_user_with_hashed_password(email=user_data.email)
    if user is None:
        raise HTTPException(status_code=401, detail=f"Пользователь с почтой {user_data.email} не зарегистрирован")
    if not AuthService().verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail=f"Неверный пароль")

    access_token = AuthService.create_access_token({"user_id": user.id, "email": user.email})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me",
            summary="Текущий пользователь")
async def only_auth(
        db: DBDep,
        user_id: UserIdDep
):
    return await db.users.get_one_or_none(id=user_id)


@router.post("/logout",
             summary="Выход из системы")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "Logged out"}
