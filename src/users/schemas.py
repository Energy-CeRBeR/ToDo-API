from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.categories.schemas import CategoryResponse
from src.tasks.schemas import TaskResponse

from src.users.models import Gender, Roles


class SuccessfulResponse(BaseModel):
    success: str = "ok"


class TokenData(BaseModel):
    short_name: str | None = None


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class UserCreate(BaseModel):
    name: str
    surname: str
    short_name: str
    email: str
    gender: Gender
    password: str


class UserEdit(BaseModel):
    name: str
    surname: str
    gender: Gender


class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    short_name: str
    email: str
    gender: Gender
    role: Roles
    is_verified: bool
    is_active: bool
    created_at: datetime
    tasks: List[TaskResponse]
    categories: List[CategoryResponse]
