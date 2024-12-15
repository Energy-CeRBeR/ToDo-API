from typing import List, Annotated
from pydantic import BaseModel, Field

from src.categories.schemas import CategoryResponse
from src.tasks.schemas import TaskResponse
from src.users.models import Gender


class SuccessfulResponse(BaseModel):
    success: str = "ok"


class TokenData(BaseModel):
    short_name: str | None = None


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class UserCreate(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50)]
    surname: Annotated[str, Field(min_length=2, max_length=50)]
    short_name: Annotated[str, Field(min_length=3, max_length=20)]
    email: Annotated[str, Field(min_length=6, max_length=50)]
    gender: Gender
    password: Annotated[str, Field(min_length=8, max_length=25)]


class UserLogin(BaseModel):
    email: Annotated[str, Field(min_length=6, max_length=50)]
    password: Annotated[str, Field(min_length=8, max_length=25)]


class UserEdit(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50)]
    surname: Annotated[str, Field(min_length=2, max_length=50)]
    gender: Gender


class UserResponse(BaseModel):
    id: int
    name: Annotated[str, Field(min_length=2, max_length=50)]
    surname: Annotated[str, Field(min_length=2, max_length=50)]
    short_name: Annotated[str, Field(min_length=3, max_length=20)]
    email: Annotated[str, Field(min_length=6, max_length=50)]
    gender: Gender
    tasks: List[TaskResponse]
    categories: List[CategoryResponse]
