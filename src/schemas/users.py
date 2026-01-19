from pydantic import BaseModel, Field, EmailStr


class UserRequest(BaseModel):
    email: EmailStr = Field(description="Электронный адрес")
    password: str = Field(description="Пароль")


class UserParams(BaseModel):
    email: EmailStr = Field(description="Электронный адрес")

    phone_number: str | None = Field(default=None, description="Номер телефона")
    first_name: str | None = Field(default=None, description="Имя пользователя")
    last_name: str | None = Field(default=None, description="Фамилия пользователя")
    username: str | None = Field(default=None, description="Никнейм пользователя")


class User(UserParams):
    id: int = Field(description="ID пользователя")


class UserAdd(UserParams):
    hashed_password: str = Field(description="Хеш-пароля")


class UserWithHashPassword(User):
    hashed_password: str = Field(description="Хеш-пароля")
