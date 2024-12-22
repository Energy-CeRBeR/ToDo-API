from typing import List, Annotated
from pydantic import BaseModel, Field

from src.tasks.schemas import TaskResponse


class SuccessfulResponse(BaseModel):
    success: str = "ok"


class CategoryCreate(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=50)]
    color: str


class CategoryEdit(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=50)]
    color: str


class CategoryResponse(BaseModel):
    id: int
    name: Annotated[str, Field(min_length=1, max_length=50)]
    color: str
    tasks: List[TaskResponse]
